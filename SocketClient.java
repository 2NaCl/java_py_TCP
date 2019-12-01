package com.techfantasy.qs.socket;

import java.io.*;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class SocketClient {

    public static void main(String[] args) throws IOException {
        try {
            Socket socket = new Socket("localhost",21567);
            while (true) {
                //获取输出流，向服务器端发送信息
                OutputStream os = socket.getOutputStream();//字节输出流
                PrintWriter pw = new PrintWriter(os);//将输出流包装为打印流
                System.out.print("> ");
                Scanner instr = new Scanner(System.in);

                pw.write(instr.nextLine());//前端要填的参数
                pw.flush();
                System.out.println("\n");
                //socket.shutdownOutput();//关闭输出流

                InputStream is = socket.getInputStream();
                BufferedReader in = new BufferedReader(new InputStreamReader(is));
                String[] s = in.readLine().split(" ");

                List<List<String>> arrlist2 = new ArrayList<>();
                for (String str : s) {
                    List<String> arrayList = new ArrayList<>();
                    arrayList.add(str);
                    arrlist2.add(arrayList);
                }
                System.out.println(arrlist2);
//                is.close();
//                in.close();
//                socket.close();
            }
        } catch (UnknownHostException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
