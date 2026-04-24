#include <iostream>
#include <fstream>
#include <string>
#include "Code File/json.hpp" // JSON header

using namespace std;
using json = nlohmann::json;

int main() {
    // 1. Load the JSON file
    ifstream inputFile("get.php.json");
    if (!inputFile.is_open()) {
        cerr << "Could not open get.php.json" << endl;
        return 1;
    }

    json data;
    inputFile >> data;
    inputFile.close();

    // 2. Open output CSV
    ofstream outputFile("hkd_rates.csv");
    outputFile << "Period,Maturity,Rate" << endl;

    // 3. Navigate the JSON structure
    // Your file has a "dataSet" array containing the data points
    auto& results = data["dataSet"];

    for (const auto& item : results) {
        string period = item["period"];
        string maturity = item["MATURITY"];
        
        // 4. Filter: Let's only grab the 3-Month rates for your specific graph
        if (maturity == "3M" && item["figure"].is_number()) {
            double rate = item["figure"];
            outputFile << period << "," << maturity << "," << rate << endl;
        }
    }

    outputFile.close();
    cout << "Successfully created hkd_rates.csv!" << endl;

    return 0;
}