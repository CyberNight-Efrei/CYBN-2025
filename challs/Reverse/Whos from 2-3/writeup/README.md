# 1

Ouvrir goodboi.ko dans ghidra et constater un hook sur netfilter : 

```c
undefined8 hook_nf_server(undefined8 param_1,long param_2)

{
  byte *pbVar1;
  undefined8 uVar2;
  int iVar3;
  short *psVar4;
  ulong uVar5;
  uint uVar6;
  undefined8 *puVar7;
  ulong *puVar8;
  long lVar9;
  long in_GS_OFFSET;
  byte bVar10;
  undefined8 uStack_b0;
  ulong uStack_a8;
  undefined8 uStack_a0;
  undefined8 uStack_98;
  undefined8 uStack_90;
  undefined8 uStack_88;
  undefined8 uStack_80;
  undefined8 uStack_78;
  undefined8 uStack_70;
  undefined8 uStack_68;
  undefined8 uStack_60;
  undefined8 uStack_58;
  undefined8 uStack_50;
  undefined8 uStack_48;
  undefined8 uStack_40;
  undefined8 uStack_38;
  undefined8 uStack_30;
  long local_28;
  
  bVar10 = 0;
  local_28 = *(long *)(in_GS_OFFSET + 0x28);
  pbVar1 = (byte *)((ulong)*(ushort *)(param_2 + 0xb8) + *(long *)(param_2 + 200));
  if (((pbVar1[9] == 6) &&
      (psVar4 = (short *)(*(long *)(param_2 + 200) + (ulong)*(ushort *)(param_2 + 0xb6)),
      *psVar4 == 21924)) && (psVar4[1] == 5632)) {
    iVar3 = (uint)(*(byte *)(psVar4 + 6) >> 4) * 4;
    uVar6 = (uint)(ushort)(*(ushort *)(pbVar1 + 2) << 8 | *(ushort *)(pbVar1 + 2) >> 8) -
            (iVar3 + (*pbVar1 & 0xf) * 4);
    if (uVar6 != 0) {
      lVar9 = 0;
      puVar7 = (undefined8 *)((long)psVar4 + (long)iVar3);
      do {
        uStack_b0 = (undefined *)0x101a73;
        _printk(&DAT_0010034a,*(undefined *)((long)puVar7 + lVar9));
        if (((int)lVar9 + 1U & 0xf) == 0) {
          uVar2 = FUN_00101dd2();
          return uVar2;
        }
        lVar9 = lVar9 + 1;
      } while ((uint)lVar9 < uVar6);
      if ((uVar6 & 0xf) != 0) {
        uStack_b0 = (undefined *)0x101e8e;
        _printk(&DAT_00100352);
      }
      uStack_a8 = 0;
      uVar5 = 0x7f;
      if (uVar6 < 0x80) {
        uVar5 = (ulong)uVar6;
      }
      uStack_a0 = 0;
      uStack_98 = 0;
      uStack_90 = 0;
      uStack_88 = 0;
      uStack_80 = 0;
      uStack_78 = 0;
      uStack_70 = 0;
      uStack_68 = 0;
      uStack_60 = 0;
      uStack_58 = 0;
      uStack_50 = 0;
      uStack_48 = 0;
      uStack_40 = 0;
      uStack_38 = 0;
      uStack_30 = 0;
      uVar6 = (uint)uVar5;
      if (uVar6 < 8) {
        if ((uVar5 & 4) == 0) {
          if (uVar6 != 0) {
            uStack_a8 = (ulong)*(byte *)puVar7;
            if ((uVar5 & 2) != 0) {
              *(undefined2 *)((long)&uStack_b0 + uVar5 + 6) =
                   *(undefined2 *)((long)puVar7 + (uVar5 - 2));
            }
          }
        }
        else {
          uStack_a8 = (ulong)*(uint *)puVar7;
          *(undefined4 *)((long)&uStack_b0 + uVar5 + 4) =
               *(undefined4 *)((long)puVar7 + (uVar5 - 4));
        }
      }
      else {
        *(undefined8 *)((long)&uStack_b0 + uVar5) = *(undefined8 *)((long)puVar7 + (uVar5 - 8));
        puVar8 = &uStack_a8;
        for (uVar5 = (ulong)(uVar6 - 1 >> 3); uVar5 != 0; uVar5 = uVar5 - 1) {
          *puVar8 = *puVar7;
          puVar7 = puVar7 + (ulong)bVar10 * -2 + 1;
          puVar8 = puVar8 + (ulong)bVar10 * -2 + 1;
        }
      }
      uStack_b0 = (undefined *)0x101e7d;
      send_message_to_thread(&uStack_a8);
    }
  }
  if (local_28 == *(long *)(in_GS_OFFSET + 0x28)) {
    return 1;
  }
                    /* WARNING: Subroutine does not return */
  uStack_b0 = &UNK_00101a8a;
  __stack_chk_fail();
}
```

# 2 

balancer le code de ghidra dans chatgpt et lui dire de reconstruire de maniere un peu plus clean le code sachant que c'est un hook de netfilter

```c
unsigned int hook_nf_server(void *priv, struct sk_buff *skb,
                            const struct nf_hook_state *state)
{
    struct iphdr  *iph;
    struct tcphdr *tcph;
    unsigned char *payload;
    unsigned int   iphdr_len, tcphdr_len, payload_len;
    unsigned char  buf[128] = {0};
    unsigned int   i;

    iph = ip_hdr(skb);
    if (iph->protocol == IPPROTO_TCP) {
        tcph = tcp_hdr(skb);

        /* Example: filter on ports */
        if (ntohs(tcph->source) == 21924 && ntohs(tcph->dest) == 5632) {

            iphdr_len   = iph->ihl * 4;
            tcphdr_len  = tcph->doff * 4;
            payload_len = ntohs(iph->tot_len) - (iphdr_len + tcphdr_len);

            if (payload_len > 0) {
                payload = (unsigned char *)((unsigned char *)tcph + tcphdr_len);

                /* Dump to printk */
                for (i = 0; i < payload_len; i++) {
                    printk(KERN_INFO "%02x ", payload[i]);
                    if (((i + 1) % 16) == 0)
                        printk(KERN_INFO "\n");
                }
                if (payload_len % 16 != 0)
                    printk(KERN_INFO "\n");

                /* Copy into buffer for user thread */
                if (payload_len > sizeof(buf))
                    payload_len = sizeof(buf);
                memcpy(buf, payload, payload_len);

                send_message_to_thread(buf);
            }
        }
    }
    return NF_ACCEPT;
}
```

On retrouve les éléments suivants : 
- proto: TCP
- port source: 21924
- port dest: 5632

sauf que chatgpt dit n'imp, le proto est bon mais pas les ports

Si on lui dit qu'il a fait une bourde avec les short int, unsigned, ... il fix comme il faut : 

```c
unsigned int hook_nf_server(void *priv, struct sk_buff *skb,
                            const struct nf_hook_state *state)
{
    struct iphdr  *iph;
    struct tcphdr *tcph;
    unsigned int   iphlen, tcphlen, paylen;
    unsigned char *payload;
    unsigned char  buf[128] = {0};   // this is what the decompiler exploded into uStack_* locals

    iph = ip_hdr(skb);
    if (!iph || iph->protocol != IPPROTO_TCP)
        return NF_ACCEPT;

    tcph = tcp_hdr(skb);
    if (!tcph)
        return NF_ACCEPT;

    /* real ports after ntohs() */
    if (ntohs(tcph->source) == 42069 && ntohs(tcph->dest) == 22) {
        iphlen  = iph->ihl * 4;
        tcphlen = tcph->doff * 4;
        paylen  = ntohs(iph->tot_len) - (iphlen + tcphlen);

        if ((int)paylen > 0) {
            payload = (unsigned char *)tcph + tcphlen;

            /* (printing omitted)… */

            if (paylen > sizeof(buf))
                paylen = sizeof(buf);
            memcpy(buf, payload, paylen);

            send_message_to_thread(buf);   // fixed-size 128-byte message
        }
    }
    return NF_ACCEPT;
}
```

# 3

Flag: CYBN{TCP:42069:22}
