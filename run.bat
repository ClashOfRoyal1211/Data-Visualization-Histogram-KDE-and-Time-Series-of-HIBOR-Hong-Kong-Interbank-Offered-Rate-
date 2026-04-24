@echo off
cd /d "%~dp0"
echo Generating HIBOR visualization...
python combined_plot.py
echo.
echo Visualization complete! View combined_rates_plot_sources.png
pause