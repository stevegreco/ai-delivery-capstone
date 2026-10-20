import { EleventyHtmlBasePlugin } from "@11ty/eleventy";

export default function (eleventyConfig) {
  // Rewrites absolute URLs ("/plan/ROADMAP/") to include the --pathprefix on GitHub Pages.
  eleventyConfig.addPlugin(EleventyHtmlBasePlugin);

  // Every markdown file in docs/ uses the base layout, so docs/ needs no front matter.
  eleventyConfig.addGlobalData("layout", "base.njk");

  // The home page lives here instead of in docs/, keeping docs/ free of site files.
  eleventyConfig.addTemplate("index.njk", "{% include 'home.njk' %}", { title: "Home" });

  // Pages in one docs/ subfolder, sorted by filename, e.g. section(collections.all, "journal").
  eleventyConfig.addFilter("section", (pages, name) =>
    pages
      .filter((p) => p.filePathStem.startsWith(`/${name}/`))
      .sort((a, b) => a.filePathStem.localeCompare(b.filePathStem))
  );

  // docs/ links to sibling files as "ISSUES.md". Eleventy outputs docs/plan/ISSUES.md
  // as /plan/ISSUES/, one folder deeper than the source, so prefix "../" and drop ".md".
  eleventyConfig.addTransform("md-links", function (content) {
    if (!(this.page.outputPath || "").endsWith(".html")) return content;
    return content.replace(
      /href="(?![a-z]+:|\/|#)([^"#]+)\.md(#[^"]*)?"/g,
      (_, path, hash = "") => `href="../${path}/${hash}"`
    );
  });

  return {
    dir: {
      input: "../docs",
      includes: "../site/_includes",
      output: "_site",
    },
    markdownTemplateEngine: false,
  };
}
