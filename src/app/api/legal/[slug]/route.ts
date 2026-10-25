import { NextRequest, NextResponse } from "next/server";
import fs from "fs";
import path from "path";

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ slug: string }> }
) {
  const { slug } = await params;

  // 1. Thông tư 89-2026
  if (slug === "tt89" || slug === "thong-tu-89-2026") {
    try {
      const htmlPath = path.join(
        process.cwd(),
        "public",
        "vbpl",
        "thong-tu-89-2026",
        "index.html"
      );
      if (fs.existsSync(htmlPath)) {
        const html = fs.readFileSync(htmlPath, "utf-8");
        return new NextResponse(html, {
          status: 200,
          headers: {
            "Content-Type": "text/html; charset=utf-8",
            "Cache-Control": "public, max-age=3600",
          },
        });
      }
    } catch (e) {
      console.error("Error reading tt89 html:", e);
    }
  }

  // 2. Check if local HTML file exists in public/legal/{slug}.html
  const localLegalFile = path.join(
    process.cwd(),
    "public",
    "legal",
    `${slug}.html`
  );
  if (fs.existsSync(localLegalFile)) {
    const html = fs.readFileSync(localLegalFile, "utf-8");
    return new NextResponse(html, {
      status: 200,
      headers: {
        "Content-Type": "text/html; charset=utf-8",
        "Cache-Control": "public, max-age=3600",
      },
    });
  }

  // 3. Fallback: proxy from production site for existing documents
  try {
    const prodUrl = `https://www.hkdkkhome.com/api/legal/${slug}`;
    const res = await fetch(prodUrl, {
      headers: {
        "User-Agent": "KKhome-App-Viewer",
      },
      next: { revalidate: 86400 },
    });

    if (res.ok) {
      const html = await res.text();
      return new NextResponse(html, {
        status: 200,
        headers: {
          "Content-Type": "text/html; charset=utf-8",
          "Cache-Control": "public, max-age=86400",
        },
      });
    }
  } catch (err) {
    console.error(`Error proxying document ${slug}:`, err);
  }

  return new NextResponse("Document not found", { status: 404 });
}
