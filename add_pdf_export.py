"""
Add PDF export option to ExportOptionsSheet across all 10 CoachBoard apps.
Each app uses the same pattern, so we just inject:
  1) pdf import
  2) PDF option in the export format list
  3) PDF generation method
"""
import os
import re

APPS = [
    ("coachboard", "coachboard", "I am The Coach - Soccer"),
    ("coachboard-basketball", "coachboard_basketball", "I am The Coach - Basketball"),
    ("coachboard-baseball", "coachboard_baseball", "I am The Coach - Baseball"),
    ("coachboard-cricket", "coachboard_cricket", "I am The Coach - Cricket"),
    ("coachboard-hockey", "coachboard_hockey", "I am The Coach - Hockey"),
    ("coachboard-volleyball", "coachboard_volleyball", "I am The Coach - Volleyball"),
    ("coachboard-handball", "coachboard_handball", "I am The Coach - Handball"),
    ("coachboard-lacrosse", "coachboard_lacrosse", "I am The Coach - Lacrosse"),
    ("coachboard-rugby", "coachboard_rugby", "I am The Coach - Rugby"),
    ("coachboard-football", "coachboard_football", "I am The Coach - Football"),
]

BASE = r"C:\Users\SMART"

PDF_METHOD_TEMPLATE = '''
  Future<void> _exportPdf(BuildContext context) async {{
    try {{
      final boundary = repaintKey.currentContext?.findRenderObject()
          as RenderRepaintBoundary?;
      if (boundary == null) {{
        if (context.mounted) {{
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(S.get('couldNotCapture'))),
          );
        }}
        return;
      }}

      final image = await boundary.toImage(pixelRatio: 3.0);
      final byteData =
          await image.toByteData(format: ui.ImageByteFormat.png);
      if (byteData == null) return;
      final bytes = byteData.buffer.asUint8List();

      final pdf = pw.Document();
      final pdfImage = pw.MemoryImage(bytes);
      pdf.addPage(
        pw.Page(
          pageFormat: pdfx.PdfPageFormat.a4,
          margin: const pw.EdgeInsets.all(24),
          build: (ctx) => pw.Center(
            child: pw.Column(
              mainAxisAlignment: pw.MainAxisAlignment.center,
              children: [
                pw.Text(
                  '{title}',
                  style: pw.TextStyle(
                    fontSize: 14,
                    fontWeight: pw.FontWeight.bold,
                  ),
                ),
                pw.SizedBox(height: 12),
                pw.Expanded(
                  child: pw.Image(pdfImage, fit: pw.BoxFit.contain),
                ),
              ],
            ),
          ),
        ),
      );

      final dir = await getTemporaryDirectory();
      final file = File(
          '${{dir.path}}/coachboard_${{DateTime.now().millisecondsSinceEpoch}}.pdf');
      await file.writeAsBytes(await pdf.save());

      await Share.shareXFiles(
        [XFile(file.path)],
        text: '{title}',
      );
    }} catch (e) {{
      if (context.mounted) {{
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(S.get('exportFailed', {{'e': '$e'}}))),
        );
      }}
    }}
  }}
'''


def patch_app(app_dir, package, title):
    path = os.path.join(BASE, app_dir,
                        "lib", "presentation", "widgets",
                        "export_options_sheet.dart")
    if not os.path.exists(path):
        print(f"  SKIP {app_dir}: no export_options_sheet.dart")
        return False

    src = open(path, encoding="utf-8").read()

    # Skip if already patched
    if "_exportPdf" in src:
        print(f"  SKIP {app_dir}: already patched")
        return True

    # 1) Add imports for pdf
    if "package:pdf/pdf.dart" not in src:
        src = src.replace(
            "import 'package:share_plus/share_plus.dart';",
            "import 'package:pdf/pdf.dart' as pdfx;\n"
            "import 'package:pdf/widgets.dart' as pw;\n"
            "import 'package:share_plus/share_plus.dart';",
        )

    # 2) Inject PDF list tile in build()
    # Find the closing of the format list and inject before
    format_list_end = "                )),\n          ],\n        ),\n      ),\n    );\n  }"
    pdf_tile = '''                )),
            const Divider(height: 24),
            ListTile(
              leading: Icon(
                Icons.picture_as_pdf,
                color: AppColors.primary,
              ),
              title: const Text('PDF Document'),
              subtitle: const Text(
                'A4 page',
                style: TextStyle(fontSize: 12),
              ),
              onTap: () {
                Navigator.pop(context);
                _exportPdf(context);
              },
            ),
          ],
        ),
      ),
    );
  }'''
    if format_list_end in src:
        src = src.replace(format_list_end, pdf_tile)
    else:
        print(f"  WARN {app_dir}: format list anchor not found, skipping UI injection")

    # 3) Add the _exportPdf method before _drawWatermark
    method_anchor = "  static void _drawWatermark("
    method_code = PDF_METHOD_TEMPLATE.format(title=title)
    if method_anchor in src and "_exportPdf" not in src:
        src = src.replace(method_anchor, method_code + "\n" + method_anchor)

    open(path, "w", encoding="utf-8").write(src)
    print(f"  [OK] {app_dir}")
    return True


def main():
    for app_dir, package, title in APPS:
        patch_app(app_dir, package, title)


if __name__ == "__main__":
    main()
