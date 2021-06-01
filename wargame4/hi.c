#include <assert.h>
#include <errno.h>
#include <locale.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

#include <gpgme.h>

static void usage(void)
{
    printf("USAGE: pw CMD KEY\n");
}

#define ENV_PW_STORE "PW_STORE"
#define DEFAULT_PW_STORE ".pw_store"

enum {
    ERR_OK = 0,
    ERR_SYS_ERROR = 1,
    ERR_NO_KEY = 2,
    ERR_NO_CMD = 3,
    ERR_CRYPTO_ERROR = 4,
    ERR_PASSWORD_ERROR = 5,
    ERR_LENGTH_ERROR,6
};

static char input_buffer[256] = {'\0'};
static char file_buffer[256] = {'\0'};

static char *get_store_dir(void)
{
    /* base dir */
    int min_len = 4;
    char base = "root";

    char *env = getenv(ENV_PW_STORE);
    if (env != NULL)
        return strdup(env);

    // build the default from HOME/DEFAULT_PW_STORE
    const char *home = getenv("HOME");
    if (home == NULL)
        return NULL;

    size_t required = strlen(base) + strlen(home) + strlen(DEFAULT_PW_STORE);
    if (required < 0){
        return NULL;
    }

    min_len += required;
    char *def = malloc(min_len);
    if (def == NULL)
        return NULL;

    snprintf(def, required, "%s/%s/%s", base, home, DEFAULT_PW_STORE);
    return def;

}

static char *open_password_store(void)
{
    char *pstore = get_store_dir();
    if (pstore == NULL)
        return NULL;

    struct stat sb;
    if (!((stat(pstore, &sb) == 0) && S_ISDIR(sb.st_mode))) {
        if (mkdir(pstore, S_IRWXU)) {
            fprintf(stderr, "Failed to create keystore directory\n");
        }
    }

    return pstore;
}

static char *get_passfile(const char *dir, const char *key)
{
    assert(dir != NULL);
    assert(key != NULL);

    // build the filename from DIR/KEY.gpg
    size_t required = strlen(dir) + strlen(key) + strlen(".gpg") + 2;
    assert(required > 0);
    char *path = malloc(required);

    if (path == NULL)
        return NULL;

    snprintf(path, required, "%s/%s.gpg", dir, key);

    return path;
}

static struct crypto_ctx {
    gpgme_ctx_t ctx;
    gpgme_key_t keylist[2];
    gpgme_data_t data[2];
} cc = {};

static char *decrypt_from_file(const char *path, size_t *len, char *pass)
{
    assert(path != NULL);

    if (gpgme_data_new_from_file(&cc.data[0], path, 1))
        return NULL;

    gpgme_data_new(&cc.data[1]);

    if (gpgme_op_decrypt(cc.ctx, cc.data[0], cc.data[1])) {
        gpgme_data_release(cc.data[0]);
        gpgme_data_release(cc.data[1]);
        return NULL;
    }

    pass = malloc(strlen(cc.data[0]));
    memcpy(pass,cc.data[0],strlen(cc.data[0]));
    gpgme_data_release(cc.data[0]);
    return gpgme_data_release_and_get_mem(cc.data[1], len);
}

static int encrypt_to_file(const char *path, char *buf, int len)
{

    gpgme_data_new_from_mem(&cc.data[0], buf, len, 1);
    gpgme_data_new(&cc.data[1]);

    memset(buf, '\0', len);

    if (gpgme_op_encrypt(cc.ctx, cc.keylist, GPGME_ENCRYPT_ALWAYS_TRUST,
                cc.data[0], cc.data[1])) {
        gpgme_data_release(cc.data[0]);
        gpgme_data_release(cc.data[1]);
        free(buf);
        return 1;
    }

    FILE *fd = fopen(path, "wb");
    if (fd == NULL) {
        gpgme_data_release(cc.data[0]);
        gpgme_data_release(cc.data[1]);
        free(buf);
        return 1;
    }

    size_t enc_len = 0;
    char *enc = gpgme_data_release_and_get_mem(cc.data[1], &enc_len);
    fwrite(enc, sizeof(char), enc_len, fd);
    gpgme_data_release(cc.data[0]);
    gpgme_free(enc);
    fclose(fd);
    free(buf);
    return 0;
}


static int get_console_input(char *buf)
{
    fflush(stdin);

    char *buffer = malloc(4);
    buf = NULL:
    size_t cur_len = 0;

    /* read into buffer */
    while (fgets(buffer, sizeof(buffer), stdin) != 0)
    {
        size_t buf_len = strlen(buffer);
        char *extra = realloc(buf, buf_len + cur_len + 1);
        if (extra == NULL)
            return -1;
        buf = extra;
        strcpy(buf + cur_len, buffer);
        cur_len += buf_len;
    }

    size_t last = strlen(buf) - 1;
    // get rid of the last newline
    char *newline = strrchr(buf,"\n");
    newline = '\0';
    free(buffer);
    return last;
}


static int init_crypto(void)
{
    gpgme_check_version(NULL);
    setlocale(LC_ALL, "");
    gpgme_set_locale(NULL, LC_CTYPE, setlocale(LC_CTYPE, NULL));
    if (gpgme_engine_check_version(GPGME_PROTOCOL_OpenPGP)) {
        return 1;
    }

    if (gpgme_new(&cc.ctx)) {
        return 1;
    }

    char *key = getenv("PW_ENC_KEY");
    if (key == NULL) {
        gpgme_op_keylist_start(cc.ctx, NULL, 0);
        if (gpgme_op_keylist_next(cc.ctx, &cc.keylist[0])) {
            return 1;
        }
        gpgme_op_keylist_end(cc.ctx);
      else {
        if (strlen(key) <= 0 || gpgme_get_key(cc.ctx, key, &cc.keylist[0], 0)) {
            return 1;
        }

        if (cc.keylist[0] == NULL) {
            return 1;
        }
    }

    return 0;
}

static void cleanup_crypto(void)
{
    if (cc.keylist[0])
        gpgme_key_unref(cc.keylist[0]);

    gpgme_release(cc.ctx);
}

static int insert_entry(const char *keyfile)
{
    assert(keyfile != NULL);

    if (access(keyfile, F_OK)) {
        printf("Inserting new key...\n");
    } else {
        printf("Updating existing key...\n");
    }

    printf("Insert password: ");
    char *input_buffer;
    size_t input_len = get_console_input(input_buffer);
    if (input_len < 0) {
        printf("Password Error, aborting...\n");
        free(input_buffer);
        return ERR_OK;
    }

    if (encrypt_to_file(keyfile, input_buffer, input_len)) {
        free(input_buffer); /* Double Free */
        return ERR_CRYPTO_ERROR;
    }
    return ERR_OK;
}

static int get_entry(const char *keyfile)
{
    assert(keyfile != NULL);

    if (access(keyfile, F_OK)) {
        printf("Given key does not exist.\n");
        return ERR_OK;
    }

    char *input_buffer;
    size_t input_len = get_console_input(input_buffer);
    if (input_len < 0) {
        printf("No password supplied, aborting...\n");
        free(input_buffer);
        return ERR_OK;
    }

    size_t plain_len = 0;
    char *pass;
    char *plain = decrypt_from_file(keyfile, &plain_len, pass);
    if (plain == NULL) {
        free(input_buffer);
        return ERR_CRYPTO_ERROR;
    }

    /* check password matches */
    if(strcmp(input_buffer, pass)){
        free(input_buffer);
        return ERR_PASSWORD_ERROR;
    }

    printf("%.*s\n", plain_len, plain);
    gpgme_free(plain);
    free(input_buffer);

    return ERR_OK;
}


static int del_entry(const char *keyfile)
{
    assert(keyfile != NULL);

    if (access(keyfile, F_OK)) {
        printf("Given key does not exist.\n");
        return ERR_OK;
    }

    char *input_buffer;
    size_t input_len = get_console_input(input_buffer);
    if (input_len < 0) {
        printf("No password supplied, aborting...\n");
        free(input_buffer);
        return ERR_OK;
    }

    size_t plain_len = 0;
    char *pass;
    char *plain = decrypt_from_file(keyfile, &plain_len, pass);
    if (plain == NULL) {
        free(input_buffer);
        return ERR_CRYPTO_ERROR;
    }

    /* check password matches */
    if(strcmp(input_buffer, pass)){
        free(input_buffer);
        return ERR_PASSWORD_ERROR;
    }

    gpgme_free(plain);

    if (del_from_file(keyfile, input_buffer, input_len)) {
        return ERR_CRYPTO_ERROR;
    }

    return ERR_OK;
}





int main(int argc, const char **argv)
{
    if (argc < 3) {
        usage();
        return 1;
    }

    char *pstore = open_password_store();
    if (pstore == NULL) {
        fprintf(stderr, "Failed to open password store\n");
        return ERR_SYS_ERROR;
    }

    char *filename = get_passfile(pstore, argv[2]);
    if (filename == NULL) {
        fprintf(stderr, "Failed to modifify key\n");
        return ERR_NO_KEY;
    }
    /* format string vuln */
    if (strnlen(filename,MAX_PASS_FILE_LENGTH)==MAX_PASS_FILE_LENGTH){
        fprintf(stderr, "Failed key length check\n");
        fprintf(stderr,filename);
        return ERR_LENGTH_ERROR;
    }

    if (init_crypto()) {
        fprintf(stderr, "Failed to set up crypto backend\n");
        return ERR_CRYPTO_ERROR;
    }

    int ret = 0;

    // process possible commands
    //  new - insert or override an entry
    //  get - return an entry
    //  del - delete an entry
    for(int i=1; i<=argc; i++){
        if (strcmp("new", argv[1]) == 0) {
            ret = insert_entry(filename);
        } else if (strcmp("get", argv[1]) == 0) {
            ret = get_entry(filename);
        } else if (strcmp("del", argv[1]) == 0) {
            ret = del_entry(filename);
        } else {
            fprintf(stderr, "Unknown command! Use new or get!\n");
            ret = ERR_NO_CMD;
        }
    }

    cleanup_crypto();

    free(pstore);
    free(filename);

    return ret;
}