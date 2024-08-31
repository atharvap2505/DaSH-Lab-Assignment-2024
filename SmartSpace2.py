import psutil
import csv
import time
from ping3 import ping

def get_system_stats():
    stats = {}
    
    stats['cpu_percent'] = psutil.Process().cpu_percent(interval=1)
    stats['num_threads'] = psutil.Process().num_threads()

    disk_io = psutil.disk_io_counters()
    stats['disk_read_bytes'] = disk_io.read_bytes
    stats['disk_write_bytes'] = disk_io.write_bytes

    net_io = psutil.net_io_counters()
    stats['bytes_sent'] = net_io.bytes_sent
    stats['bytes_recv'] = net_io.bytes_recv
    
    return stats


def get_network_stats(host='8.8.8.8'):
    stats = {}
    latency = ping(host)
    if latency is not None:
        stats['latency_ms'] = latency * 1000  #latency in ms
    else:
        stats['latency_ms'] = 'N/A'  
    stats['packet_loss'] = 1 if latency is None else 0 #if packet is lost
    return stats

def write_to_csv(file_name, data):
    with open(file_name, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if file.tell() == 0: #empty file means write header
            writer.writeheader()
        writer.writerow(data)

def main():
    file_name = 'system_network_stats.csv'
    interval = 4  # +1 seconds
    duration = 60  # Total duration to run the script 
    start_time = time.time()

    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time > duration:
            print("Finished collecting data.")
            break
        
        system_stats = get_system_stats()
        network_stats = get_network_stats()

        stats = {**system_stats, **network_stats}
        stats['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
        
        write_to_csv(file_name, stats)
        time.sleep(interval)

main()
