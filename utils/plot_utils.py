import plotly.graph_objects as go

def plot_signals(df, signals):
    """
    Visualiser lysestager og signaler på et diagram.
    """
    fig = go.Figure()

    # Lysestager
    fig.add_trace(go.Candlestick(
        x=df['time'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name="Candlesticks"
    ))

    # Signalpunkter
    for i, signal in enumerate(signals):
        if signal == 'buy':
            fig.add_trace(go.Scatter(
                x=[df['time'].iloc[i]],
                y=[df['low'].iloc[i]],
                mode='markers',
                marker=dict(color='green', size=10),
                name='Buy Signal'
            ))
        elif signal == 'sell':
            fig.add_trace(go.Scatter(
                x=[df['time'].iloc[i]],
                y=[df['high'].iloc[i]],
                mode='markers',
                marker=dict(color='red', size=10),
                name='Sell Signal'
            ))

    fig.update_layout(title="Trading Signals", xaxis_title="Time", yaxis_title="Price")
    fig.show()