#include <windows.h>
#define LIB "\\libraries\\Courses.exe\""

int main(void) {
	system("title Loading Program...");
    char cwd[MAX_PATH], path[MAX_PATH] = "";
    char* szEnd;
    path[0] = '"';
    GetModuleFileNameA(NULL, cwd, MAX_PATH);
    szEnd = strrchr(cwd, '\\');
    *szEnd = 0;
    strcat_s(path, MAX_PATH, cwd);
    strcat_s(path, MAX_PATH, LIB);
    system(path);
    return 0;
}