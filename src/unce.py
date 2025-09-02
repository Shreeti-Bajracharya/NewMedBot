from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

from document_chat import extract_text_from_pdf, create_vector_store, query_with_context

app = Flask(__name__)
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
 8. AJAX Chat Interaction (chat.html JavaScript)
javascript
Copy
Edit
$("#messageArea").on("submit", function(event) {
    var rawText = $("#text").val();
    $("#text").val("");

    $.ajax({
        data: { msg: rawText },
        type: "POST",
        url: "/get",
    }).done(function(data) {
        var botHtml = '<div class="msg_cotainer">' + data + '</div>';
        $("#messageFormeight").append(botHtml);
    });

    event.preventDefault();
});