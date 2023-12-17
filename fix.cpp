#include <fstream>

int main(int argc, char* argv[]) {
    std::string file = argv[1];
    std::ifstream fin("data/" + file + ".csv");
    std::string result = "id,cab_type,pickup_datetime,dropoff_datetime,passenger_count,trip_distance,rate_code_id,store_and_fwd_flag,pu_location_id,do_location_id,payment_type,fare_amount,extra,mta_tax,tip_amount,tolls_amount,improvement_surcharge,total_amount,congestion_surcharge,airport_fee\n";
    std::string line;
    std::getline(fin, line);
    while (std::getline(fin, line)) {
        unsigned long long find;
        if ((find = line.find(",,")) != std::string::npos)
            line.replace(find, 2, ",");
        if (line.back() == ',')
            line.replace(line.size()-1, 1, "");
        result += line + '\n';
    }
    fin.close();
    FILE *fout = fopen(("data/" + file + "_fix.csv").c_str(), "w");
    fwrite(result.data(), 1, result.size(), fout);
    fclose(fout);
    return 0;
}
