#include <iostream>
#include <fstream>

using namespace std;

int main(int argc, char* argv[]) {
    string file = argv[1];
    ifstream fin(file + ".csv");
    string result = "id,cab_type,pickup_datetime,dropoff_datetime,passenger_count,trip_distance,rate_code_id,store_and_fwd_flag,pu_location_id,do_location_id,payment_type,fare_amount,extra,mta_tax,tip_amount,tolls_amount,improvement_surcharge,total_amount,congestion_surcharge,airport_fee\n";
    string line;
    getline(fin, line);
    while (getline(fin, line)) {
        unsigned long long find;
        if ((find = line.find(",,")) != string::npos)
            line.replace(find, 2, ",");
        if (line.back() == ',')
            line.replace(line.size()-1, 1, "");
        result += line + '\n';
    }
    fin.close();
    FILE *fout = fopen((file + "_fix.csv").c_str(), "w");
    fwrite(result.data(), 1, result.size(), fout);
    fclose(fout);
    return 0;
}
