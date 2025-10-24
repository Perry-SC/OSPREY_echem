# Changelog

All notable changes to this project will be documented in this file.

## [1.3.1] - 2025-10-24
### Added
- Changed the graph plotting functions so that graphs are visualised internally using FigureCanvasTkAgg, rather than relying on exporting and importing png files with Matplotlib

## [1.3.0] - 2025-10-23
### Added
- Added a scrollbar to dynamically increase the font size in the worksheet window
- Added a button to dynamically change the background colour between white and a softer off-yellow

## [1.2.0] - 2025-09-09
### Added
- Added the name of the practical into the exported PDF filename to prevent issues with multiple smart worksheets being used for different practicals

### Fixed
- Bug that meant the scrollbar did not recognise when a widget had changed size. 

## [1.1.0] - 2025-08-13
### Added
- Function to export a PDF summary of student scores.
- Two new questions added to the assessment module.

### Fixed
- Bug in reporting numerical values to the correct number of significant figures.

## [1.0.0] - 2025-04-02
### Added
- Initial release of the smart worksheet for chemistry assessments.
