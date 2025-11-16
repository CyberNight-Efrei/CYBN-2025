#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <sys/socket.h>

// Pseudo header for TCP checksum calculation
struct pseudo_header {
    u_int32_t src_addr;
    u_int32_t dst_addr;
    u_int8_t placeholder;
    u_int8_t protocol;
    u_int16_t tcp_length;
};

// Checksum function
unsigned short csum(unsigned short *ptr, int nbytes) {
    long sum = 0;
    unsigned short oddbyte;

    while (nbytes > 1) {
        sum += *ptr++;
        nbytes -= 2;
    }
    if (nbytes == 1) {
        oddbyte = 0;
        *((u_char *) &oddbyte) = *(u_char *) ptr;
        sum += oddbyte;
    }

    sum = (sum >> 16) + (sum & 0xffff);
    sum += sum >> 16;
    const short answer = (short) ~sum;

    return answer;
}

int main(const int argc, char *argv[]) {
    if (argc != 6) {
        fprintf(stderr, "Usage: %s <ip source> <port source> <ip distant> <port distant> <command>\n", argv[0]);
        return EXIT_FAILURE;
    }

    char *ip_src = argv[1];
    int port_src = atoi(argv[2]);

    char *ip_dst = argv[3];
    int port_dst = atoi(argv[4]);

    char *message = argv[5];

    const int s = socket(AF_INET, SOCK_RAW, IPPROTO_RAW);
    if (s < 0) {
        perror("socket");
        exit(1);
    }

    int one = 1;
    if (setsockopt(s, IPPROTO_IP, IP_HDRINCL, &one, sizeof(one)) < 0) {
        perror("setsockopt");
        exit(1);
    }

    char datagram[4096] = {0};

    // IP header
    const auto iph = (struct iphdr *) datagram;
    // TCP header
    const auto tcph = (struct tcphdr *) (datagram + sizeof(struct iphdr));
    // Data
    char *data = datagram + sizeof(struct iphdr) + sizeof(struct tcphdr);
    strcpy(data, message);

    struct sockaddr_in sin;
    sin.sin_family = AF_INET;
    sin.sin_port = htons(port_src);
    sin.sin_addr.s_addr = inet_addr(ip_dst);

    // Fill IP header
    iph->ihl = 5;
    iph->version = 4;
    iph->tos = 0;
    iph->tot_len = htons(sizeof(struct iphdr) + sizeof(struct tcphdr) + strlen(data));
    iph->id = htonl(54321);
    iph->frag_off = 0;
    iph->ttl = 64;
    iph->protocol = IPPROTO_TCP;
    iph->check = 0; // Kernel does not fill this for raw IP
    iph->saddr = inet_addr(ip_src); // <-- change to your source IP
    iph->daddr = sin.sin_addr.s_addr;

    // Fill TCP header
    tcph->source = htons(port_src);
    tcph->dest = htons(port_dst);
    tcph->seq = 0; //htonl(1);
    tcph->ack_seq = 0;
    tcph->doff = 5; // header size
    tcph->fin = 0;
    tcph->syn = 1;
    tcph->rst = 0;
    tcph->psh = 0; // we’re pushing data without handshake
    tcph->ack = 0;
    tcph->urg = 0;
    tcph->window = htons(5840); // max window size
    tcph->check = 0; // filled later
    tcph->urg_ptr = 0;

    // TCP checksum
    struct pseudo_header psh;
    psh.src_addr = iph->saddr;
    psh.dst_addr = iph->daddr;
    psh.placeholder = 0;
    psh.protocol = IPPROTO_TCP;
    psh.tcp_length = htons(sizeof(struct tcphdr) + strlen(data));

    int psize = sizeof(struct pseudo_header) + sizeof(struct tcphdr) + strlen(data);
    char *pseudogram = malloc(psize);

    memcpy(pseudogram, &psh, sizeof(struct pseudo_header));
    memcpy(pseudogram + sizeof(struct pseudo_header), tcph, sizeof(struct tcphdr) + strlen(data));

    tcph->check = csum((unsigned short *) pseudogram, psize);

    free(pseudogram);

    // Send the packet
    if (sendto(s, datagram, ntohs(iph->tot_len), 0, (struct sockaddr *) &sin, sizeof(sin)) < 0) {
        perror("sendto failed");
    } else {
        printf("Raw TCP packet sent to %s:%d from port %s:%d with data: %s\n", ip_dst, port_dst, ip_src, port_src, message);
    }

    close(s);
    return 0;
}
