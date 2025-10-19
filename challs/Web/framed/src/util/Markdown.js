const { marked } = require("marked");
const { Renderer } = marked;

const renderer = new Renderer();

renderer.code = function(code, lang) {
    if (lang == "lead") return "<p class=\"lead\">" + code + "</p>";
    if (lang == "muted-lead") return "<p class=\"lead text-muted\">" + code + "</p>";
    if (lang == "small") return "<small>" + code + "</small>";
    if (lang == "small-muted") return "<small class=\"text-muted\">" + code + "</small>";
    if (lang == "term") return "<span class=\"term\">" + code + "</span>";
    return new Renderer().code.apply(this, arguments);
};

marked.use({ renderer });

module.exports = marked;