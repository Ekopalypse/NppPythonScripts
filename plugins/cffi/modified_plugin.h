#ifndef CFFI_DLLEXPORT
#  if defined(_MSC_VER)
#    define CFFI_DLLEXPORT  extern __declspec(dllimport)
#  else
#    define CFFI_DLLEXPORT  extern
#  endif
#endif

typedef uintptr_t uptr_t;
typedef intptr_t sptr_t;
typedef ptrdiff_t Sci_Position;

typedef struct _Sci_NotifyHeader{
	/* Compatible with Windows NMHDR.
	 * hwndFrom is really an environment specific window handle or pointer
	 * but most clients of Scintilla.h do not have this type visible. */
	void *hwndFrom;
	uptr_t idFrom;
	unsigned int code;
} Sci_NotifyHeader;

typedef struct _SCNotification{
	Sci_NotifyHeader nmhdr;
	Sci_Position position;
	/* SCN_STYLENEEDED, SCN_DOUBLECLICK, SCN_MODIFIED, SCN_MARGINCLICK, */
	/* SCN_NEEDSHOWN, SCN_DWELLSTART, SCN_DWELLEND, SCN_CALLTIPCLICK, */
	/* SCN_HOTSPOTCLICK, SCN_HOTSPOTDOUBLECLICK, SCN_HOTSPOTRELEASECLICK, */
	/* SCN_INDICATORCLICK, SCN_INDICATORRELEASE, */
	/* SCN_USERLISTSELECTION, SCN_AUTOCSELECTION */

	int ch;
	/* SCN_CHARADDED, SCN_KEY, SCN_AUTOCCOMPLETED, SCN_AUTOCSELECTION, */
	/* SCN_USERLISTSELECTION */
	int modifiers;
	/* SCN_KEY, SCN_DOUBLECLICK, SCN_HOTSPOTCLICK, SCN_HOTSPOTDOUBLECLICK, */
	/* SCN_HOTSPOTRELEASECLICK, SCN_INDICATORCLICK, SCN_INDICATORRELEASE, */

	int modificationType;	/* SCN_MODIFIED */
	const char *text;
	/* SCN_MODIFIED, SCN_USERLISTSELECTION, SCN_AUTOCSELECTION, SCN_URIDROPPED */

	Sci_Position length;		/* SCN_MODIFIED */
	Sci_Position linesAdded;	/* SCN_MODIFIED */
	int message;	/* SCN_MACRORECORD */
	uptr_t wParam;	/* SCN_MACRORECORD */
	sptr_t lParam;	/* SCN_MACRORECORD */
	Sci_Position line;		/* SCN_MODIFIED */
	int foldLevelNow;	/* SCN_MODIFIED */
	int foldLevelPrev;	/* SCN_MODIFIED */
	int margin;		/* SCN_MARGINCLICK */
	int listType;	/* SCN_USERLISTSELECTION */
	int x;			/* SCN_DWELLSTART, SCN_DWELLEND */
	int y;		/* SCN_DWELLSTART, SCN_DWELLEND */
	int token;		/* SCN_MODIFIED with SC_MOD_CONTAINER */
	Sci_Position annotationLinesAdded;	/* SCN_MODIFIED with SC_MOD_CHANGEANNOTATION */
	int updated;	/* SCN_UPDATEUI */
	int listCompletionMethod;  /* SCN_AUTOCSELECTION, SCN_AUTOCCOMPLETED, SCN_USERLISTSELECTION, */
} SCNotification;

typedef const TCHAR * (__cdecl * PFUNCGETNAME)();

typedef struct _NppData{
	HWND _nppHandle;
	HWND _scintillaMainHandle;
	HWND _scintillaSecondHandle;
} NppData;

typedef void (__cdecl * PFUNCSETINFO)(NppData);
typedef void (__cdecl * PFUNCPLUGINCMD)(void);
typedef void (__cdecl * PBENOTIFIED)(SCNotification *);
typedef LRESULT (__cdecl * PMESSAGEPROC)(UINT Message, WPARAM wParam, LPARAM lParam);

typedef struct ShortcutKey{
	BOOL _isCtrl;
	BOOL _isAlt;
	BOOL _isShift;
	UCHAR _key;
}ShortcutKey;

typedef struct FuncItem{
	TCHAR _itemName[64];  // nbChar
	PFUNCPLUGINCMD _pFunc;
	int _cmdID;
	BOOL _init2Check;
	struct ShortcutKey *_pShKey;
} FuncItem;

typedef FuncItem * (__cdecl * PFUNCGETFUNCSARRAY)(int *);

// You should implement (or define an empty function body) those functions which are called by Notepad++ plugin manager
CFFI_DLLEXPORT void setInfo(NppData);
CFFI_DLLEXPORT const TCHAR * getName();
CFFI_DLLEXPORT FuncItem * getFuncsArray(int *nbF);
CFFI_DLLEXPORT void beNotified(SCNotification *);
CFFI_DLLEXPORT LRESULT messageProc(UINT Message, WPARAM wParam, LPARAM lParam);

// This API return always true now, since Notepad++ isn't compiled in ANSI mode anymore
CFFI_DLLEXPORT BOOL isUnicode();


