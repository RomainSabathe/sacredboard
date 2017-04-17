import plotly
import numpy as np
import plotly.tools as tls
import matplotlib.pyplot as plt


colors = ['#e74c3c', '#3498db', '#2ecc71', '#9b59b6', '#f39c12', '#2c3e50',
          '#bdc3c7']


def get_idx_last_minibatch(record):
    return len(record['info']['train_minibatch_losses'])


def get_X_Y_from_record(record, stage):
    """stage is 'train' or 'val'."""
    if stage == 'train':
        X = np.arange(0, get_idx_last_minibatch(record), 1) * 1e-3
        Y = record['info']['train_minibatch_losses']
    elif stage == 'val':
        validate_every = record['config']['validate_every']
        X = np.arange(validate_every, get_idx_last_minibatch(record),
                      validate_every) * 1e-3
        Y = record['info']['val_epoch_scores']

    return X, Y


def plot_records(records):
    fig, ax = plt.subplots()
    #fig.subplots_adjust(left=0.2, bottom=0.2, right=0.8, top=0.9)
    #ax.set_xlabel(r'Minibatch ($\times 10^3$)')

    all_lines = []
    for ii, record in enumerate(records):
        experiment_name = record['experiment']['name']
        if ii >= len(colors):
            continue
        color = colors[ii]

        # Training loss.
        X, Y = get_X_Y_from_record(record, 'train')
        all_lines.extend(ax.plot(
            X, Y,
            label='{}'.format(experiment_name),
            c=color,
            linewidth=0.7,
            alpha=0.5))
        ax.set_ylabel('CTC loss')
        #ax.tick_params('y', colors='#3498db')
        ax.set_yscale('log')

    # Validation score
    ax_right = ax.twinx()
    for ii, record in enumerate(records):
        experiment_name = record['experiment']['name']
        if ii >= len(colors):
            continue
        color = colors[ii]
        X, Y = get_X_Y_from_record(record, 'val')
        ax_right.plot(
            X, Y,
            #label='Val score - {}'.format(experiment_name),
            c=color,
            marker='D',
            linewidth=0.7,
            markersize=2.)
        ax_right.set_ylabel('Levenshtein score')
        #ax_right.tick_params('y', colors='#e74c3c')
        ax_right.set_yscale('log')
        #ax_right.set_ylim([0.04, 0.055])

    # Legend
    #all_lines = line_train + line_test
    #all_lines = line_test
    #labels = [l.get_label() for l in all_lines]
    #legend = ax.legend(all_lines, labels, frameon=True)
    #legend.get_frame().set_facecolor('#FFFFFF')

    ax.grid(True)
    plotly_fig = tls.mpl_to_plotly(fig)
    plotly.offline.plot(plotly_fig)
