#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
using namespace std;

int main() {
    ifstream inputFile("../Table 340-45022_en.csv");
    ofstream outputFile("hibor_processed.csv");

    if (!inputFile.is_open()) {
        cout << "Error" << endl;
        return 1;
    }

    string line;
    outputFile << "Date,% ThreeMonthRate" << endl;

    // Skip the 7 rows of title and metadata in the CSV
    for(int i = 0; i < 7; ++i) getline(inputFile, line);

    while (getline(inputFile, line)) {
        stringstream ss(line);
        string year, quarter, overnight, oneWeek, oneMonth, threeMonth;
        getline(ss, year, ',');
        getline(ss, quarter, ',');
        getline(ss, overnight, ',');
        getline(ss, oneWeek, ',');
        getline(ss, oneMonth, ',');
        getline(ss, threeMonth, ',');
        // DATA CLEANING LOGIC:
        // 1. Only grab rows where 'quarter' is NOT empty (this ignores the annual totals)
        // 2. Ensure the threeMonth rate is a number, not "N.A."
        if (!quarter.empty() && threeMonth != "N.A." && !threeMonth.empty()) {
            string period = year + "-" + quarter;
            outputFile << period << "," << threeMonth << endl;
        }
    }

    inputFile.close();
    outputFile.close();

    cout << "Created hibor_processed.csv" << endl;
    return 0;
}