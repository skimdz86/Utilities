package it.test.mail;
 
import java.util.Date;
import java.util.Properties;
 
import javax.activation.DataHandler;
import javax.activation.FileDataSource;
import javax.mail.Address;
import javax.mail.Message;
import javax.mail.MessagingException;
import javax.mail.Multipart;
import javax.mail.Session;
import javax.mail.Transport;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeBodyPart;
import javax.mail.internet.MimeMessage;
import javax.mail.internet.MimeMultipart;
 
 
/**
 * @author MDZ Class for sending emails
 */
public class GenericMailSender {
      private StringBuffer message = new StringBuffer();
      
      
      /**
     * Append the message passed from parameter to class variable for email message
     * 
     * @param message
     *            Partial message to append to email message before sending email.
     */
    public void appendMessage(String message) {
        this.message.append(message);
    }
 
    /**
     * Clear the message
     * 
     */
    public void clearMessage() {
        this.message = new StringBuffer();
    }
 
      /**
       * Send an email with multiple to, cc, bcc an one single attachment (for now). 
       * @param to Lista di indirizzi separata da ;
       * @param cc Lista di indirizzi cc separata da ;
       * @param bcc Lista di indirizzi ccn separata da ;
       * @param from Mittente
       * @param replyTo Indirizzo per il reply
       * @param mailServer Indirizzo del mailserver con credenziali (user e password opzionali)
       * @param subject Oggetto della mail
       * @param sendAttachment Indica se il messaggio contiene attachments
       * @param attachment Path in cui recuperare l'allegato
       */
	public boolean sendMail(String to, String cc, String bcc, String from, String replyTo, MailServer mailServer, String subject, boolean sendAttachment, String attachment) {
		try {

			// Create properties, get Session
			Properties props = new Properties();

			// If using static Transport.send(), need to specify which host to
			// send it to
			props.put("mail.smtp.host", mailServer.getHost());

			if (mailServer.getUser() != null && !mailServer.getUser().equals("")) props.setProperty("mail.user", mailServer.getUser());
			if (mailServer.getPwd() != null && !mailServer.getPwd().equals("")) props.setProperty("mail.password", mailServer.getPwd());

			// To see what is going on behind the scene
			// props.put("mail.debug", "true");
			props.put("mail.smtp.sendpartial", true);// invia anche se alcuni degli indirizzi non sono validi
			Session session = Session.getInstance(props);

			try {
				// Instantiate a message
				Message msg = new MimeMessage(session);

				// Set message attributes
				msg.setFrom(new InternetAddress(from));

				// Set reply-to
				Address[] replyAddresses = new Address[1];
				replyAddresses[0] = new InternetAddress(replyTo);
				msg.setReplyTo(replyAddresses);

				// Set to
				String[] multipleTo = to.split(";");
				int sizeTo = multipleTo.length;

				if (sizeTo == 0)
					throw new MessagingException("No address specified");

				InternetAddress[] addressTo;
				addressTo = new InternetAddress[sizeTo];
				for (int i = 0; i < sizeTo; i++) {
					addressTo[i] = new InternetAddress(multipleTo[i]);
				}

				msg.setRecipients(Message.RecipientType.TO, addressTo);

				// Set cc
				String[] multipleCc = cc.split(";");
				int sizeCc = multipleCc.length;

				InternetAddress[] addressCc;
				addressCc = new InternetAddress[sizeCc];
				for (int i = 0; i < sizeCc; i++) {
					addressCc[i] = new InternetAddress(multipleCc[i]);
				}

				if (sizeCc > 0)	msg.setRecipients(Message.RecipientType.CC, addressCc);

				// Set bcc : blind cc
				String[] multipleBcc = bcc.split(";");
				int sizeBcc = multipleBcc.length;

				InternetAddress[] addressBcc;
				addressBcc = new InternetAddress[sizeBcc];
				for (int i = 0; i < sizeBcc; i++) {
					addressBcc[i] = new InternetAddress(multipleBcc[i]);
				}

				if (sizeBcc > 0) msg.setRecipients(Message.RecipientType.BCC, addressBcc);

				// set subject
				msg.setSubject(subject);
				msg.setSentDate(new Date());

				Multipart mp = new MimeMultipart();

				// crea e compila la prima parte del messaggio
				MimeBodyPart mbp1 = new MimeBodyPart();
				mbp1.setText(message.toString());
				mp.addBodyPart(mbp1);

				if (sendAttachment) {
					// crea la sewconda parte del messaggio
					MimeBodyPart mbp2 = new MimeBodyPart();

					FileDataSource fds = new FileDataSource(attachment);
					mbp2.setDataHandler(new DataHandler(fds));
					mbp2.setFileName(fds.getName());
					mp.addBodyPart(mbp2);
				}

				// per aggiungere ulteriori allegati, replicare l'if qui sopra e
				// aggiungere al Multipart

				msg.setContent(mp);

				// Set message content
				// msg.setContent(message.toString(), "text/html");

				// Send the message
				Transport.send(msg);
			} catch (MessagingException mex) {
				// Prints all nested (chained) exceptions as well
				mex.printStackTrace();
				return false;
			}

		} catch (Exception e) {
			// throw new Exception();
			e.printStackTrace();
			return false;
		}
		return true;

	}
      
      /**
       * Permette di specificare un cluster di mail server a cui inviare la mail: se fallisce la chiamata al primo si passa al secondo e così via
       * */
      public void sendMailWithFailover(String to, String cc, String bcc, String from, String replyTo, MailServer[] mailServers, String subject, boolean sendAttachment, String attachment){
          if(mailServers.length>0){
              boolean messageSent = false;
              int counter = 0;
              while(!messageSent){
                  System.out.println("COUNTER "+counter);
                  messageSent = sendMail(to, cc, bcc, from, replyTo, mailServers[counter], subject, sendAttachment, attachment);
                  counter++;
              }
          }
      }
      
	private class MailServer {
		private String host, user, pwd;

		public MailServer(String host) {
			this.host = host;
			this.user = null;
			this.pwd = null;
		}

		public MailServer(String host, String user, String pwd) {
			this.host = host;
			this.user = user;
			this.pwd = pwd;
		}

		public String getHost() {
			return host;
		}

		public void setHost(String host) {
			this.host = host;
		}

		public String getUser() {
			return user;
		}

		public void setUser(String user) {
			this.user = user;
		}

		public String getPwd() {
			return pwd;
		}

		public void setPwd(String pwd) {
			this.pwd = pwd;
		}

	}
      
      
      
      
      public static void main(String[] args) throws Exception{
    	  GenericMailSender mail = new GenericMailSender();
          mail.testMail();
      }
      
      public void testMail(){
        System.out.println("Version 5");
        String to = "";
        String cc = "";
        String bcc = "";//blind cc
        String from = "";
        MailServer[] servers = new MailServer[2];
        servers[0] = new MailServer("");
        servers[1] = new MailServer("");
        String subject = "TEST";
        String replyTo = "";
        appendMessage("Messaggio di prova");
//      sendMail(to, cc, bcc, from, replyTo, host, subject, false, null);
        sendMailWithFailover(to, cc, bcc, from, replyTo, servers, subject, false, null);
    }
}
