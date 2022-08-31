#include "gnss_synchro_udp_source.h"
#include "gnss_synchro.pb.h"
#include <sstream>
#include <ncurses.h>

Gnss_Synchro_Udp_Source::Gnss_Synchro_Udp_Source(const unsigned short port) :
    socket{io_service},
    endpoint{boost::asio::ip::udp::v4(), port}
{
    socket.open(endpoint.protocol(), error);  // Open socket.
    socket.bind(endpoint, error);             // Bind the socket to the given local endpoint.
}


bool Gnss_Synchro_Udp_Source::read_gnss_synchro(gnss_sdr::Observables& stocks)
{
    char buff[1500];  // Buffer for storing the received data.

    // This call will block until one or more bytes of data has been received.
    int bytes = socket.receive(boost::asio::buffer(buff));

    std::string data(&buff[0], bytes);
    // Deserialize a stock of Gnss_Synchro objects from the binary string.
    return stocks.ParseFromString(data);
}

void Gnss_Synchro_Udp_Source::populate_channels(gnss_sdr::Observables& stocks)
{
    for (std::size_t i = 0; i < stocks.observable_size(); i++)
        {
            gnss_sdr::GnssSynchro ch = stocks.observable(i);
            if (ch.fs() != 0)  // Channel is valid.
                {
                    channels[ch.channel_id()] = ch;
                }
        }
}


bool Gnss_Synchro_Udp_Source::print_table(std::string& log)
{
    log = "";
    if (read_gnss_synchro(stocks))
        {
            populate_channels(stocks);

            clear();  // Clear the screen.

            // Print table header.
            attron(A_REVERSE);
            printw("%3s%6s%10s%17s%14s%14s\n", "CH", "PRN", "Prompt_i", "Prompt_q", "CN0 [dB-Hz]", "Doppler [Hz]");
            attroff(A_REVERSE);

            for(auto const& ch: channels)
            {
                int channel_id = ch.first;  
                gnss_sdr::GnssSynchro data = ch.second; 

                printw("%3d%6d%10d%17f%14f%14f\n", channel_id, data.prn(), (int)data.prompt_i(), data.prompt_q(), data.cn0_db_hz(), data.carrier_doppler_hz());
                std::string line;
                line.resize(71);
                sprintf((char*)line.c_str(), "%3d,%6d,%10d,%17f,%14f,%14f, ", channel_id, data.prn(), (int)data.prompt_i(), data.prompt_q(), data.cn0_db_hz(), data.carrier_doppler_hz());
                log += line;
            }

            refresh();  // Update the screen.

        }
    else
        {
            return false;
        }

    return true;
}

