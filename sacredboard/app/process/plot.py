import plotly
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as tls
import matplotlib.pyplot as plt


colors = ['#e74c3c', '#3498db', '#2ecc71', '#9b59b6', '#f39c12', '#2c3e50',
          '#bdc3c7']


def get_idx_last_minibatch(record):
    return len(record['info']['train_minibatch_losses'])


def get_X_Y_from_record(record, stage):
    """stage is 'train' or 'val'."""
    if stage == 'train':
        X = [idx_and_loss[0] for idx_and_loss in record['info']['train_losses']]
        Y = [idx_and_loss[1] for idx_and_loss in record['info']['train_losses']]
    else:  # For now, it's only stage == 'val'
        X = [idx_and_score[0] for idx_and_score in record['info']['val_scores']]
        Y = [idx_and_score[1] for idx_and_score in record['info']['val_scores']]

    return X, Y


def plot_records(records):
    data = []
    records = sorted(records, key=lambda record: int(record['_id']))
    try:
        for i, record in enumerate(records):
            X, Y = get_X_Y_from_record(record, 'train')
            trace_train = go.Scatter(
                x=X,
                y=Y,
                mode='lines',
                name=format(record['experiment']['name']),
                yaxis='yaxis data',
                line=dict(
                    color=colors[i],
                ),
                opacity=1./len(records) * 0.5
            )
            data.append(trace_train)

            X, Y = get_X_Y_from_record(record, 'val')
            y = []
            smoothing = 10
            for j in range(len(Y[:(-smoothing)])):
                val = np.mean(Y[j:j+smoothing])
                y.append(val)
            X = np.linspace(0, X[-1], len(y))
            Y = np.array(y)
            trace_val = go.Scatter(
                x=X,
                y=Y,
                mode='lines+markers',
                name=format(record['experiment']['name']),
                yaxis='y2',
                line=dict(
                    color=colors[i],
                ),
                opacity=0.7
            )
            data.append(trace_val)

        layout = go.Layout(
            title='Loss over minibatches',
            xaxis=dict(
                title='Minibatches'
            ),
            yaxis=dict(
                title='CTC loss',
                type='log'
            ),
            yaxis2=dict(
                title='Normalized Levenshtein distance',
                overlaying='y',
                side='right',
                type='log'
            )
        )

        fig = go.Figure(data=data, layout=layout)
        plotly.offline.plot(fig)
    except Exception as e:
        print(e)
        import pdb; pdb.set_trace()
        pass

