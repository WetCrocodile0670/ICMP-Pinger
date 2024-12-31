from scapy.all import IP, ICMP, sr1
import asyncio
import argparse

async def send_ping(target_ip, payload_size, timeout=1):

    packet = IP(dst=target_ip)/ICMP()/("X" * payload_size)
    reply = sr1(packet, timeout=timeout, verbose=False)
    if reply:
        print(f"Reply from {reply.src}: bytes={len(reply)} time={reply.time * 1000:.2f}ms")
    else:
        print(f"Request timed out for {target_ip}")

async def icmp_pinger(target_ip, payload_size, count=4, interval=1, timeout=1):
    for _ in range(count):
        await send_ping(target_ip, payload_size, timeout)
        await asyncio.sleep(interval)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fast ICMP Pinger")
    parser.add_argument("target_ip", type=str, help="Target IP Address")
    parser.add_argument("--payload_size", type=int, default=32, help="Size of ICMP load")
    parser.add_argument("--count", type=int, default=4, help="Number of pings")
    parser.add_argument("--interval", type=float, default=1, help="Interval between pings in second")
    parser.add_argument("--timeout", type=float, default=1, help="timeout for each ping in second")
    args = parser.parse_args()

    asyncio.run(icmp_pinger(args.target_ip, args.payload_size, args.count, args.interval, args.timeout))