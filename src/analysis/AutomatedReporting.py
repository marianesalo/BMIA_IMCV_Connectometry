import os
import pandas as pd

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    PageBreak
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from matplotlib import pyplot as plt

class AautomatedReporting:
    def __init__(
        self,
        demographics_csv,
        dsi_result_txt,
        output_dir,
        study_variables,
        report_title="Connectometry Analysis Report"
    ):
        self.demographics_csv = demographics_csv
        self.dsi_result_txt = dsi_result_txt
        self.output_dir = output_dir
        self.study_variables = study_variables
        self.report_title = report_title

        self.figures_dir = os.path.join(output_dir, "figures")
        self.report_dir = os.path.join(output_dir, "reports")

        os.makedirs(self.figures_dir, exist_ok=True)
        os.makedirs(self.report_dir, exist_ok=True)

        self.styles = getSampleStyleSheet()

        self.df_demo = None
        self.df_dsi = None

        self.variable_summaries = []
        self.generated_plots = []
    

    def load_data(self):
        """
        Load demographics and DSI result data from specified files.
        """
        print("Loading demographics CSV...")
        self.df_demo = pd.read_csv(self.demographics_csv)

        print("Loading DSI result file...")
        self.df_dsi = pd.read_csv(
            self.dsi_result_txt,
            sep=r"\s+",
            engine="python"
        )

        print("Data loaded successfully.")

    
    def compute_variable_summaries(self):
        """
        Compute summary statistics for each study variable
        """
        print("Computing study variable summaries...")
        for var in self.study_variables:
            if var not in self.df_demo.columns:
                print(f"WARNING: {var} not found.")
                continue

            if pd.api.types.is_numeric_dtype(self.df_demo[var]):
                summary = {
                    "Variable": var,
                    "Type": "Numeric",
                    "Mean": round(self.df_demo[var].mean(), 2),
                    "Std": round(self.df_demo[var].std(), 2),
                    "Min": round(self.df_demo[var].min(), 2),
                    "Max": round(self.df_demo[var].max(), 2),
                }

            else:
                summary = {
                    "Variable": var,
                    "Type": "Categorical",
                    "Unique Values": self.df_demo[var].nunique()
                }

            self.variable_summaries.append(summary)


    def generate_distribution_plots(self):
        """
        Generate distribution plots for each study variable
        and save them to the figures directory.
        """
        print("Generating plots...")
        for var in self.study_variables:
            if var not in self.df_demo.columns:
                continue
            plt.figure(figsize=(8, 5))

            if pd.api.types.is_numeric_dtype(self.df_demo[var]):

                plt.hist(self.df_demo[var], bins=10)

                plt.xlabel(var)
                plt.ylabel("Count")
                plt.title(f"{var} Distribution")

            else:

                self.df_demo[var].value_counts().plot(kind="bar")
                plt.xlabel(var)
                plt.ylabel("Count")
                plt.title(f"{var} Distribution")

            plot_path = os.path.join(
                self.figures_dir,
                f"{var}_distribution.png"
            )

            plt.savefig(plot_path, bbox_inches="tight")
            plt.close()

            self.generated_plots.append((var, plot_path))

    
    def generate_connectometry_plots(self):
        """
        Generate plots summarizing DSI connectometry results,
        such as FDR vs voxel distance, significant tracks vs voxel distance,
        and observed vs null tracks.
        """
        print("Generating connectometry plots...")

        # FDR vs voxel distance
        if ("voxel_dis" in self.df_dsi.columns and "fdr_inc" in self.df_dsi.columns):

            plt.figure(figsize=(8, 5))
            plt.plot(
                self.df_dsi["voxel_dis"],
                self.df_dsi["fdr_inc"],
                marker="o"
            )
            plt.xlabel("Voxel Distance Threshold")
            plt.ylabel("FDR")
            plt.title("FDR vs Tract Length Threshold")
            plt.grid(True)

            fdr_plot_path = os.path.join(
                self.figures_dir,
                "fdr_vs_tract_length.png"
            )

            plt.savefig(
                fdr_plot_path,
                bbox_inches="tight"
            )
            plt.close()

            self.generated_plots.append(
                ("FDR vs Tract Length", fdr_plot_path)
            )

        # Significant tracks vs voxel distance
        if (
            "voxel_dis" in self.df_dsi.columns
            and "#track_inc" in self.df_dsi.columns
        ):

            plt.figure(figsize=(8, 5))
            plt.plot(
                self.df_dsi["voxel_dis"],
                self.df_dsi["#track_inc"],
                marker="o"
            )
            plt.xlabel("Voxel Distance Threshold")
            plt.ylabel("Significant Tracks")
            plt.title("Significant Tracks Across Thresholds")
            plt.grid(True)

            tracks_plot_path = os.path.join(
                self.figures_dir,
                "significant_tracks.png"
            )

            plt.savefig(
                tracks_plot_path,
                bbox_inches="tight"
            )
            plt.close()

            self.generated_plots.append(
                ("Significant Tracks", tracks_plot_path)
            )

        # Observed vs null tracks
        if (
            "voxel_dis" in self.df_dsi.columns
            and "#track_inc" in self.df_dsi.columns
            and "#track_inc_null" in self.df_dsi.columns
        ):

            plt.figure(figsize=(8, 5))
            plt.plot(
                self.df_dsi["voxel_dis"],
                self.df_dsi["#track_inc"],
                label="Observed"
            )
            plt.plot(
                self.df_dsi["voxel_dis"],
                self.df_dsi["#track_inc_null"],
                label="Null"
            )
            plt.xlabel("Voxel Distance Threshold")
            plt.ylabel("Track Count")
            plt.title("Observed vs Null Track Counts")
            plt.legend()
            plt.grid(True)

            null_plot_path = os.path.join(
                self.figures_dir,
                "observed_vs_null.png"
            )

            plt.savefig(null_plot_path, bbox_inches="tight")
            plt.close()

            self.generated_plots.append(
                ("Observed vs Null", null_plot_path)
            )

    def summarize_dsi_results(self):

        print("Summarizing DSI results...")
        summary = {}

        if "#track_inc" in self.df_dsi.columns:
            summary["max_track_inc"] = self.df_dsi["#track_inc"].max()

        if "#track_dec" in self.df_dsi.columns:
            summary["max_track_dec"] = self.df_dsi["#track_dec"].max()

        if "fdr_inc" in self.df_dsi.columns:
            summary["min_fdr_inc"] = self.df_dsi["fdr_inc"].replace(0,pd.NA).min()

        self.dsi_summary = summary


    def build_pdf_report(self):
        """
        Build a PDF report summarizing the connectometry analysis results,
        including demographic variable summaries, distribution plots, and DSI results.
        """
        print("Building PDF report...")
        pdf_path = os.path.join(
            self.report_dir,
            "connectometry_report.pdf"
        )

        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=letter
        )

        elements = []
        title = Paragraph(
            self.report_title,
            self.styles["Title"]
        )

        elements.append(title)
        elements.append(Spacer(1, 20))

        # ======================================================
        # INTRODUCTION
        # ======================================================
        intro = Paragraph(
            """
            This report summarizes a DSI Studio connectometry
            analysis performed using diffusion MRI-derived
            local connectome data.

            The pipeline includes:
            <br/><br/>
            - demographic variable ingestion<br/>
            - statistical connectometry analysis<br/>
            - automated summary generation<br/>
            - visualization of study variable distributions
            """,
            self.styles["BodyText"]
        )

        elements.append(intro)
        elements.append(Spacer(1, 20))

        # demographic variable summary table
        elements.append(
            Paragraph(
                "Demographic Variable Summary",
                self.styles["Heading1"]
            )
        )

        table_data = [
            ["Variable", "Type", "Mean", "Std", "Min", "Max"]
        ]

        for s in self.variable_summaries:
            if s["Type"] == "Numeric":
                table_data.append([
                    s["Variable"],
                    s["Type"],
                    str(s["Mean"]),
                    str(s["Std"]),
                    str(s["Min"]),
                    str(s["Max"]),
                ])

        table = Table(table_data)

        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 20))

        # distribution plots for study variables
        elements.append(
            Paragraph(
                "Study Variable Distributions",
                self.styles["Heading1"]
            )
        )

        for var_name, fig_path in self.generated_plots:
            elements.append(
                Paragraph(
                    f"{var_name} Distribution",
                    self.styles["Heading2"]
                )
            )
            elements.append(
                Image(
                    fig_path,
                    width=400,
                    height=250
                )
            )

            elements.append(Spacer(1, 20))


        # dsi results summary
        elements.append(PageBreak())
        elements.append(
            Paragraph(
                "Connectometry Results Summary",
                self.styles["Heading1"]
            )
        )

        dsi_text = f"""
        <br/>
        Maximum increasing tracks detected:
        {self.dsi_summary.get("max_track_inc", "N/A")}
        <br/><br/>

        Maximum decreasing tracks detected:
        {self.dsi_summary.get("max_track_dec", "N/A")}
        <br/><br/>

        Minimum FDR increase value:
        {self.dsi_summary.get("min_fdr_inc", "N/A")}
        """

        elements.append(
            Paragraph(
                dsi_text,
                self.styles["BodyText"]
            )
        )

        elements.append(Spacer(1, 20))

        # build the pdf
        doc.build(elements)
        print(f"PDF report saved to:\n{pdf_path}")

    def run(self):
        """
        Run the full automated reporting pipeline, including data loading,
        summary computation, plot generation, and PDF report building.
        """

        self.load_data()
        self.compute_variable_summaries()
        self.generate_distribution_plots()
        self.summarize_dsi_results()
        self.generate_connectometry_plots()
        self.build_pdf_report()
        print("\nPipeline completed successfully.")


if __name__ == "__main__":
    # put here the path for your repository root (where you have the data and src folders)
    REPO_ROOT = None # /path/to/your/repo/root
    if REPO_ROOT is None:
        REPO_ROOT = os.getcwd()  # default to current working directory
        REPO_ROOT = REPO_ROOT.replace("/src/analysis", "")  # adjust if running from src/analysis
    # put here the path for your demographics csv
    DEMOGRAPHICS_CSV = f"{REPO_ROOT}/data/hcp/fake_demographics.csv"
    # put here the path for your DSI result txt file
    DSI_RESULT_TXT = f"{REPO_ROOT}/data/hcp/dsi_outputs/bmi_age_sex.fdr_dist.values.txt"
    # put here the path for your output directory to save the report
    OUTPUT_DIR = f"{REPO_ROOT}/data/hcp/results"
    # put here the list of study variables you want to include in the report
    # (must match columns in demographics csv)
    STUDY_VARIABLES = [
        "bmi",
        "age",
        "sex(0=F 1=M)"
    ]

    generator = AautomatedReporting(
        demographics_csv=DEMOGRAPHICS_CSV,
        dsi_result_txt=DSI_RESULT_TXT,
        output_dir=OUTPUT_DIR,
        study_variables=STUDY_VARIABLES,
        report_title="Local Connectome Connectometry Report"
    )

    generator.run()