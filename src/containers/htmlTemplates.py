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
h2 {
padding: 0.1rem;
}
"""

bot_template = """
<div class="chat-message bot">
    <div class="message">{{MSG}}</div>
</div>
"""

trading_view_template = """
<div class="tradingview-widget-container">
    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
    {
    "autosize": true,
    "symbol": "NYSE:{{ticker}}",
    "interval": "D",
    "timezone": "Etc/UTC",
    "theme": "light",
    "width": "100%",
    "height": "100%",
    "style": "1",
    "locale": "en",
    "enable_publishing": false,
    "allow_symbol_change": false,
    "calendar": false,
    "support_host": "https://www.tradingview.com",
    "container_id": "tradingview_b9e4a",
    "studies_overrides": {
      "rsi.rsi.plot.color": "#2196f3",
      "rsi.level.0": 20,
      "rsi.level.1": 80
    },
    "studies": [
        "RSI@tv-basicstudies"
    ]
    }
    </script>
</div>
"""
