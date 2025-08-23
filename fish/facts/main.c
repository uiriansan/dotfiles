#include <sqlite3.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <time.h>
#include <unistd.h>

const char *DB_PATH = "./facts.db";

typedef struct {
  char *text;
  char *thumb_url;
  char *url;
} Page;

typedef struct {
  char *text;
  unsigned int year;
  // Page pages[];
} Fact;

static void parse_pages(char *pages, Page *page_array) {}

int main(int argc, char **argv) {
  sqlite3 *db;
  int rc = sqlite3_open(DB_PATH, &db);
  if (rc != SQLITE_OK) {
    fprintf(stderr, "Cannot open database: %s\n", sqlite3_errmsg(db));
    sqlite3_close(db);
    return 1;
  }

  sqlite3_stmt *stmt;
  const char *sql = "SELECT text, year, pages FROM Facts WHERE type LIKE "
                    "'selected' AND day LIKE ? AND month LIKE "
                    "? ORDER BY RANDOM() LIMIT 1;";

  rc = sqlite3_prepare_v2(db, sql, -1, &stmt, 0);
  if (rc != SQLITE_OK) {
    printf("[ERROR]: Failed to prepare SQL query: %s\n", sqlite3_errmsg(db));
    sqlite3_close(db);
    return 1;
  }
  time_t t = time(NULL);
  struct tm *tm_info = localtime(&t);
  sqlite3_bind_int(stmt, 1, tm_info->tm_mday);
  sqlite3_bind_int(stmt, 2, tm_info->tm_mon + 1);

  Fact fact = {.text = "", .year = 0};
  rc = sqlite3_step(stmt);
  if (rc == SQLITE_ROW) {
    fact.text = strdup((const char *)sqlite3_column_text(stmt, 0));
    fact.year = sqlite3_column_int(stmt, 1);
    // parse_pages(strdup((const char *)sqlite3_column_text(stmt, 2)),
    // fact.pages);
  } else {
    printf("[ERROR]: Failed to retrieve data.\n");
    sqlite3_close(db);
    return 1;
  }
  sqlite3_finalize(stmt);

  printf("Text: %s\nYear: %d\n", fact.text, fact.year);

  free(fact.text);
  sqlite3_close(db);

  struct winsize w;
  ioctl(STDOUT_FILENO, TIOCGWINSZ, &w);

  // for (size_t i = 0; i < 10; i++) {
  //   for (size_t j = 0; j < w.ws_col; j++) {
  //     printf("=");
  //   }
  //   printf("\n");
  // }

  // printf("%dx%d\n", w.ws_row, w.ws_col);

  return 0;
}
