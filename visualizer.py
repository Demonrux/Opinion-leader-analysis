import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import pandas as pd
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"
SUBS = [
        ('2022-05', 2967), ('2022-06', 3087), ('2022-07', 3291), ('2022-08', 3489),
        ('2022-09', 6151), ('2022-10', 7225), ('2022-11', 7029), ('2022-12', 7119),
        ('2023-01', 8443), ('2023-02', 8197), ('2023-03', 20278), ('2023-04', 17039),
        ('2023-05', 15171), ('2023-06', 13911), ('2023-07', 13952), ('2023-08', 13651),
        ('2023-09', 13603), ('2023-10', 14065), ('2023-11', 17267), ('2023-12', 19730),
        ('2024-01', 18009), ('2024-02', 16809), ('2024-03', 17664), ('2024-04', 17428),
        ('2024-05', 17364), ('2024-06', 17222), ('2024-07', 16781), ('2024-08', 16577),
        ('2024-09', 16987), ('2024-10', 18338), ('2024-11', 20439), ('2024-12', 20396),
        ('2025-01', 20141), ('2025-02', 19815), ('2025-03', 19498), ('2025-04', 19269),
        ('2025-05', 18721), ('2025-06', 18151), ('2025-07', 17625), ('2025-08', 17173),
        ('2025-09', 16789), ('2025-10', 16563), ('2025-11', 16355), ('2025-12', 16622),
        ('2026-01', 16317), ('2026-02', 16589), ('2026-03', 16426), ('2026-04', 16220),
        ('2026-05', 16149),
    ]

COLORS = {
    'count': '#FF6B6B',
    'views': '#4ECDC4',
    'confidence': '#95E77E',
    'growth': '#2ECC71',
    'decline': '#E74C3C',
    'neutral': '#95A5A6',
}


class Visualizer:
    def __init__(self, source, output_dir=REPORTS_DIR, colors=None):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.colors = colors if colors else COLORS
        self.df = self._load_data(source)
        print(f"Загружено {len(self.df)} постов")

    @staticmethod
    def _load_data(source) -> pd.DataFrame:
        if isinstance(source, str):
            with open(source, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return pd.DataFrame(data)
        elif isinstance(source, pd.DataFrame):
            return source.copy()
        else:
            raise TypeError("source должен быть str (путь к JSON) или pd.DataFrame")

    def plot_topics_distribution(self, save=True, show=True):
        significant = self.df[self.df['is_social'] == True].copy()
        if len(significant) == 0:
            print("Нет социально значимых постов")
            return

        significant['topic_short'] = significant['topic'].apply(
            lambda x: x[:30] + '...' if len(x) > 30 else x
        )
        topic_counts = significant['topic_short'].value_counts()

        plt.figure(figsize=(12, 6))
        bars = plt.bar(range(len(topic_counts)), topic_counts.values, color=self.colors['count'])
        plt.title('Социально значимые темы', fontsize=14, fontweight='bold')
        plt.xlabel('Тема')
        plt.ylabel('Количество постов')
        plt.xticks(range(len(topic_counts)), topic_counts.index, rotation=45, ha='right')

        for bar, val in zip(bars, topic_counts.values):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                     str(val), ha='center', va='bottom', fontsize=10)

        plt.tight_layout()
        if save:
            plt.savefig(self.output_dir / 'topics_distribution.png', dpi=150)
            print(f"Сохранено: {self.output_dir}/topics_distribution.png")
        if show:
            plt.show()
        plt.close()

    def plot_views_by_topic(self, save=True, show=True):
        significant = self.df[self.df['is_social'] == True].copy()
        if len(significant) == 0:
            return

        significant['topic_short'] = significant['topic'].apply(
            lambda x: x[:30] + '...' if len(x) > 30 else x
        )
        topic_views = significant.groupby('topic_short')['views'].sum().sort_values(ascending=False)

        plt.figure(figsize=(12, 6))
        bars = plt.bar(range(len(topic_views)), topic_views.values, color=self.colors['views'])
        plt.title('Просмотры по темам', fontsize=14, fontweight='bold')
        plt.xlabel('Тема')
        plt.ylabel('Всего просмотров')
        plt.xticks(range(len(topic_views)), topic_views.index, rotation=45, ha='right')

        for bar, val in zip(bars, topic_views.values):
            label = f'{val / 1000:.1f}K' if val >= 1000 else str(val)
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                     label, ha='center', va='bottom', fontsize=9)

        plt.tight_layout()
        if save:
            plt.savefig(self.output_dir / 'topics_views.png', dpi=150)
            print(f"Сохранено: {self.output_dir}/topics_views.png")
        if show:
            plt.show()
        plt.close()

    def plot_timeline_with_points(self, save=True, show=True):
        if 'date' not in self.df.columns:
            print("Нет данных о датах")
            return

        df_plot = self.df[self.df['is_social'] == True].copy()
        if len(df_plot) == 0:
            print("Нет социально значимых постов для хронологии")
            return

        df_plot['date'] = pd.to_datetime(df_plot['date'], errors='coerce')
        df_plot = df_plot.dropna(subset=['date'])
        df_plot = df_plot.sort_values('date')
        df_plot = df_plot.tail(100).copy()

        if len(df_plot) == 0:
            return

        topics = df_plot['topic'].unique()
        colors = plt.cm.Set3(range(len(topics)))
        topic_colors = {topic: colors[i] for i, topic in enumerate(topics)}

        plt.figure(figsize=(16, 8))

        min_views = df_plot['views'].min()
        max_views = df_plot['views'].max()
        if max_views > min_views:
            sizes = 50 + (df_plot['views'] - min_views) / (max_views - min_views) * 350
        else:
            sizes = [100] * len(df_plot)

        plt.scatter(df_plot['date'], range(len(df_plot)),
                    s=sizes, c=[topic_colors[t] for t in df_plot['topic']],
                    alpha=0.7, edgecolors='black', linewidth=0.8, zorder=2)

        top_posts = df_plot.nlargest(5, 'views')
        for _, post in top_posts.iterrows():
            idx = df_plot[df_plot['date'] == post['date']].index[0]
            y_pos = df_plot.index.get_loc(idx)
            views_k = post['views'] / 1000
            plt.annotate(f'{views_k:.0f}K',
                         xy=(post['date'], y_pos),
                         xytext=(5, 5), textcoords='offset points',
                         fontsize=8, fontweight='bold', color='darkred',
                         bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.7))

        plt.yticks([])
        plt.xlabel('Дата', fontsize=12)
        plt.ylabel('Посты', fontsize=10, alpha=0.7)
        plt.title('Хронология социально значимых постов', fontsize=14, fontweight='bold')

        legend_elements = [plt.Line2D([0], [0], marker='o', color='w',
                                      markerfacecolor=topic_colors[t],
                                      markersize=10, label=t[:30]) for t in topics]
        plt.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1, 1), fontsize=9)
        plt.grid(axis='x', alpha=0.3, linestyle='--')
        plt.tight_layout()

        if save:
            plt.savefig(self.output_dir / 'timeline_points.png', dpi=150, bbox_inches='tight')
            print(f"Сохранено: {self.output_dir}/timeline_points.png")
        if show:
            plt.show()
        plt.close()

    def plot_subscribers_vs_views(self, save=True, show=True):
        df_subs = pd.DataFrame(SUBS, columns=['date', 'subscribers'])
        df_subs['date'] = pd.to_datetime(df_subs['date'] + '-01')
        df_subs = df_subs.sort_values('date')
        min_date = df_subs['date'].min()

        df_plot = self.df.copy()
        df_plot['date'] = pd.to_datetime(df_plot['date'], errors='coerce')
        if df_plot['date'].dt.tz is not None:
            df_plot['date'] = df_plot['date'].dt.tz_localize(None)
        df_plot = df_plot.dropna(subset=['date'])
        df_plot = df_plot.sort_values('date')
        df_plot = df_plot[df_plot['date'] >= min_date]

        if len(df_plot) == 0:
            print("Нет данных по постам за указанный период")
            return

        df_plot['year_month'] = df_plot['date'].dt.to_period('M')
        monthly_views = df_plot.groupby('year_month')['views'].sum().reset_index()
        monthly_views['year_month'] = monthly_views['year_month'].dt.to_timestamp()
        monthly_views['views'] = monthly_views['views'] / 1000

        top_posts = df_plot.nlargest(5, 'views')
        max_subs = df_subs['subscribers'].max()

        fig, ax1 = plt.subplots(figsize=(16, 9))

        for i in range(len(df_subs) - 1):
            x = [df_subs['date'].iloc[i], df_subs['date'].iloc[i + 1]]
            y = [df_subs['subscribers'].iloc[i], df_subs['subscribers'].iloc[i + 1]]
            if y[1] > y[0]:
                color = 'green'
            elif y[1] < y[0]:
                color = 'red'
            else:
                color = 'gray'
            ax1.plot(x, y, color=color, linewidth=2.5, marker='o', markersize=6)

        ax1.set_xlabel('Дата', fontsize=12)
        ax1.set_ylabel('Подписчики', fontsize=12)

        ax2 = ax1.twinx()
        ax2.bar(monthly_views['year_month'], monthly_views['views'], color='#A23B72', alpha=0.5, width=25, label='Сумма просмотров за месяц (тыс.)')
        ax2.set_ylabel('Сумма просмотров за месяц (тыс.)', fontsize=12, color='#A23B72')
        ax2.tick_params(axis='y', labelcolor='#A23B72')

        def format_k(x):
            return f'{x / 1000:.0f}K'

        ax1.yaxis.set_major_formatter(plt.FuncFormatter(format_k))
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.0f}K'))

        for idx, (_, post) in enumerate(top_posts.iterrows()):
            views_k = post['views'] // 1000
            text_preview = post['text'][:50].replace('\n', ' ')

            closest_idx = (df_subs['date'] - post['date']).abs().argsort()[:1].values[0]
            subs_at_post = df_subs.iloc[closest_idx]['subscribers']

            if subs_at_post > max_subs * 0.8:
                y_offset = -40 - (idx % 3) * 20
                va = 'top'
            else:
                y_offset = 40 + (idx % 3) * 20
                va = 'bottom'

            ax1.annotate(
                f"{views_k}K\n{text_preview}...",
                xy=(post['date'], subs_at_post),
                xytext=(0, y_offset),
                textcoords='offset points',
                ha='center', va=va, fontsize=8,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='gold', alpha=0.9, edgecolor='orange'),
                arrowprops=dict(arrowstyle='->', color='darkorange', lw=1.5, alpha=0.8)
            )

        max_annotation_y = max_subs + 300
        current_ylim = ax1.get_ylim()
        if max_annotation_y > current_ylim[1]:
            ax1.set_ylim(current_ylim[0], max_annotation_y)

        legend_elements = [
            Patch(facecolor='green', edgecolor='green', label='Рост подписчиков'),
            Patch(facecolor='red', edgecolor='red', label='Падение подписчиков'),
        ]
        ax1.legend(handles=legend_elements, loc='upper left')
        ax2.legend(loc='upper right')

        ax1.set_title('Динамика подписчиков и виральность контента',
                      fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        plt.tight_layout()

        if save:
            plt.savefig(self.output_dir / 'subscribers_vs_views.png', dpi=150, bbox_inches='tight')
            print(f"Сохранено: {self.output_dir}/subscribers_vs_views.png")
        if show:
            plt.show()
        plt.close()

    def create_dashboard(self):
        self.plot_topics_distribution()
        self.plot_views_by_topic()

        if 'date' in self.df.columns and self.df['date'].notna().any():
            self.plot_timeline_with_points()
            self.plot_subscribers_vs_views()
        else:
            print("Нет данных подписчиков, пропускаем график")

        print(f"Дашборд сохранён в '{self.output_dir}/'")
