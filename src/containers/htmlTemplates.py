css = """
<style>
.block-container{
  padding: 1rem;
}
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}

.st-emotion-cache-16txtl3{
  padding: 1rem;
}
.st-emotion-cache-fta39a{
  gap: 0px;
}

.item-box {
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 10px;
    margin-bottom: 10px;
    background-color: #f9f9f9;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.item-link {
    margin-bottom: 5px;
}

.item-link a {
    color: #007bff;
    text-decoration: none;
}

.item-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.item-text {
    flex: 1;
}

.item-text p {
    margin: 0;
}

.line1 {
    font-weight: bold;
}

.line2 {
    color: #666;
}

.cite-button {
    padding: 5px 10px;
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 3px;
    cursor: pointer;
}
</style>
"""

item_template = """
<div class="item-box">
    <div class="item-link">
        <a href="{{URL}}" target="_blank">{{URL}}</a>
    </div>
    <div class="item-content">
        <div class="item-text">
            <p class="line1">{{LINE1}}</p>
        </div>
        <div class="item-button">
            <button class="cite-button">
                <i class="fas fa-plus-circle"></i>
            </button>
        </div>
    </div>
</div>
"""
