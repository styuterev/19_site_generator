$(document).ready(function() {
    $(".btn-article").click(function() {
        $("#articles").children().hide();
        var article_selector = "div." + this.id;
        $(article_selector).show();
    });
});