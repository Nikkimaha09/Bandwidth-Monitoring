import psutil
import time

def get_wifi_interface():
    """Check if Wi-Fi is connected and return the interface name."""
    for interface, addrs in psutil.net_if_addrs().items():
        if interface.lower().startswith("wlan") or "wi-fi" in interface.lower():
            return interface
    return None

def get_network_info(interface):
    """Get the network stats for a specific interface."""
    net_io = psutil.net_io_counters(pernic=True)
    if interface in net_io:
        return net_io[interface].bytes_sent, net_io[interface].bytes_recv
    return None, None

def format_speed(speed_in_bytes):
    """Format the speed for human readability, choosing KB/s or MB/s."""
    if speed_in_bytes >= 1024 ** 2:  # If speed >= 1 MB/s
        return f"{speed_in_bytes / (1024 ** 2):.2f} MB/s"
    else:  # If speed < 1 MB/s
        return f"{speed_in_bytes / 1024:.2f} KB/s"

def monitor_wifi_bandwidth(interval=1, max_iterations=5):
    """Monitors the Wi-Fi bandwidth usage and stops after a certain number of iterations."""
    wifi_interface = get_wifi_interface()
    
    if not wifi_interface:
        print("No Wi-Fi connection found!")
        return

    print(f"Monitoring bandwidth for interface: {wifi_interface}...")
    
    sent_prev, recv_prev = get_network_info(wifi_interface)
    iteration_count = 0

    while iteration_count < max_iterations:
        time.sleep(interval)  # wait for the next interval (in seconds)
        sent_curr, recv_curr = get_network_info(wifi_interface)

        if sent_curr is None or recv_curr is None:
            print("Error: Unable to fetch network stats for the Wi-Fi interface.")
            break

        # Calculate the bandwidth usage (sent and received) during the interval
        sent_speed = (sent_curr - sent_prev) / interval  # in bytes per second
        recv_speed = (recv_curr - recv_prev) / interval  # in bytes per second

        # Format the speeds dynamically based on their magnitude
        formatted_sent_speed = format_speed(sent_speed)
        formatted_recv_speed = format_speed(recv_speed)

        print(f"Upload Speed: {formatted_sent_speed} | Download Speed: {formatted_recv_speed}")

        # Update previous values for next iteration
        sent_prev, recv_prev = sent_curr, recv_curr
        iteration_count += 1  # Increment the iteration count

    print("Monitoring completed.")

if __name__ == "__main__":
    monitor_wifi_bandwidth(interval=1, max_iterations=5)
