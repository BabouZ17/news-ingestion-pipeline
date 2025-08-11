from datetime import datetime, timedelta
from random import randint

from fake_news_api.models.news import News

NEWS: list[News] = [
    News(
        id="1",
        source="hackernoon",
        title="The Rise of Ransomware Attacks",
        body="Ransomware attacks have become increasingly common in recent years, with hackers targeting businesses, governments, and individuals alike. These attacks involve encrypting sensitive data and demanding payment in exchange for the decryption key. The rise of ransomware attacks can be attributed to the growing use of cryptocurrencies, which provide a convenient and anonymous way for hackers to receive payments. To protect against ransomware attacks, it's essential to implement robust cybersecurity measures, including regular backups, software updates, and employee training.",
        published_at=datetime(year=2025, month=1, day=1),
    ),
    News(
        id="2",
        source="google",
        title="Google Cloud Outage Causes Widespread Disruptions",
        body="A recent outage at Google Cloud caused disruptions to several popular services, including Gmail, Google Drive, and YouTube. The outage was attributed to a technical issue with Google's network infrastructure. The incident highlighted the importance of cloud infrastructure and the need for robust disaster recovery plans. Google apologized for the outage and promised to take steps to prevent similar incidents in the future.",
        published_at=datetime(year=2025, month=2, day=4),
    ),
    News(
        id="3",
        source="yoga-society",
        title="The Benefits of Meditation for Mental Health",
        body="Meditation has long been recognized as a valuable tool for improving mental health. By reducing stress and anxiety, meditation can help individuals develop a greater sense of well-being and resilience. Regular meditation practice has also been shown to improve sleep quality, boost mood, and enhance cognitive function. With the growing demands of modern life, meditation provides a valuable opportunity for individuals to take a step back, relax, and recharge.",
        published_at=datetime(year=2023, month=12, day=10),
    ),
    News(
        id="4",
        source="cyber-news",
        title="The Importance of Password Management",
        body="Password management is a critical aspect of cybersecurity, with weak passwords providing an easy entry point for hackers. To protect against password-related threats, it's essential to implement robust password management practices, including the use of unique, complex passwords and regular password updates. Password managers can also provide a convenient and secure way to store and generate passwords.",
        published_at=datetime.now(),
    ),
    News(
        id="5",
        source="datacenter-world",
        title="Power Grid Failure Causes Widespread Blackouts",
        body="A recent power grid failure caused widespread blackouts across several states, leaving millions without electricity. The incident highlighted the importance of grid resilience and the need for robust infrastructure. Investigators attributed the failure to a combination of technical and human factors. Utility companies promised to take steps to prevent similar incidents in the future.",
        published_at=datetime(year=2024, month=7, day=1),
    ),
    News(
        id="6",
        source="better-health",
        title="The Benefits of Regular Exercise for Physical Health",
        body="Regular exercise provides numerous benefits for physical health, including weight management, improved cardiovascular health, and enhanced muscle strength. Exercise also reduces the risk of chronic diseases, such as diabetes and certain types of cancer. With the growing demands of modern life, regular exercise provides a valuable opportunity for individuals to take care of their physical health.",
        published_at=datetime(year=2022, month=2, day=2),
    ),
    News(
        id="7",
        source="cyberspace",
        title="The Rise of Phishing Attacks",
        body="Phishing attacks have become increasingly common in recent years, with hackers targeting businesses, governments, and individuals alike. These attacks involve tricking individuals into revealing sensitive information, such as login credentials or financial information. To protect against phishing attacks, it's essential to implement robust cybersecurity measures, including employee training and email filtering.",
        published_at=datetime(year=2024, month=3, day=4),
    ),
    News(
        id="8",
        source="microsoft",
        title="Microsoft Azure Outage Causes Disruptions to Cloud Services",
        body="A recent outage at Microsoft Azure caused disruptions to several cloud services, including Azure Storage and Azure Virtual Machines. The outage was attributed to a technical issue with Microsoft's network infrastructure. The incident highlighted the importance of cloud infrastructure and the need for robust disaster recovery plans. Microsoft apologized for the outage and promised to take steps to prevent similar incidents in the future.",
        published_at=datetime(year=2024, month=10, day=12),
    ),
    News(
        id="9",
        source="better-self",
        title="The Benefits of Mindfulness for Mental Health",
        body="Mindfulness has long been recognized as a valuable tool for improving mental health. By reducing stress and anxiety, mindfulness can help individuals develop a greater sense of well-being and resilience. Regular mindfulness practice has also been shown to improve sleep quality, boost mood, and enhance cognitive function. With the growing demands of modern life, mindfulness provides a valuable opportunity for individuals to take a step back, relax, and recharge.",
        published_at=datetime(year=2024, month=2, day=2),
    ),
    News(
        id="10",
        source="cyber-world",
        title="The Importance of Software Updates",
        body="Software updates are a critical aspect of cybersecurity, with outdated software providing an easy entry point for hackers. To protect against software-related threats, it's essential to implement robust software update practices, including regular updates and patching. This can help prevent cyber attacks and protect sensitive data.",
        published_at=datetime.now() - timedelta(days=10),
    ),
    # False positives
    News(
        id="11",
        source="false-positive",
        title="The importance of family",
        body="When discussing the importance of strong foundations, one might think of cybersecurity and protecting against digital threats. However, the most crucial foundation is often the one we take for granted - our family. A supportive family provides the necessary environment for growth, learning, and development. It teaches us valuable life skills like respect, empathy, and responsibility. A family's influence on our lives cannot be overstated. From our parents, we learn essential values like honesty, kindness, and hard work. Our siblings provide companionship, support, and a sense of belonging. The bonds we form with our family members are lifelong and play a significant role in shaping our personalities.",
        published_at=datetime(year=2025, month=2, day=15),
    ),
    News(
        id="12",
        source="false-positive",
        title="The benefits of a balanced diet",
        body="At first glance, the phrase 'balanced diet' might evoke thoughts of system maintenance or software updates. Yet, a balanced diet is essential for maintaining our physical and mental well-being. Eating a variety of nutrient-rich foods provides our bodies with the necessary fuel to function optimally. A well-balanced diet reduces stress, promotes healthy weight management, and boosts our energy levels. It also helps prevent chronic diseases like diabetes, heart disease, and certain types of cancer. By making informed food choices, we can significantly improve our overall health and quality of life.",
        published_at=datetime(year=2025, month=3, day=1),
    ),
    News(
        id="13",
        source="false-positive",
        title="The value of history",
        body="The term 'system update' might come to mind when thinking about the importance of history. However, history is more than just a record of past events - it's a rich tapestry of human experiences, achievements, and lessons learned. Studying history helps us understand the complexities of human nature, the consequences of our actions, and the importance of learning from our mistakes. By examining historical events, we gain valuable insights into the social, cultural, and economic contexts that shaped our world. We also develop critical thinking skills, analytical abilities, and a deeper appreciation for the diversity of human experiences. Ultimately, history teaches us that our actions have consequences and that we must learn from the past to build a better future.",
        published_at=datetime(year=2020, month=1, day=1),
    ),
    # False negatives
    News(
        id="14",
        source="false-negative",
        title="The art of navigation",
        body="Navigating unfamiliar territories requires a combination of skills, including observation, analysis, and decision-making. A navigator must be able to read signs, identify patterns, and adapt to changing circumstances. These skills are essential for anyone who wants to stay safe and secure in today's digital landscape. In the world of cybersecurity, navigation is critical. Cyber threats are constantly evolving, and security experts must be able to navigate complex systems, identify vulnerabilities, and respond quickly to emerging threats. By developing strong navigation skills, individuals can improve their ability to protect themselves and their organizations from cyber threats.",
        published_at=datetime(year=2025, month=6, day=30),
    ),
    News(
        id="15",
        source="false-negative",
        title="The resilience of ecosystems",
        body="Ecosystems are complex networks of relationships between living organisms and their environment. They are constantly adapting to changes in their surroundings, and they have developed remarkable strategies for resilience and survival. One of the key factors that contributes to the resilience of ecosystems is diversity. In the context of IT systems, diversity is also essential for resilience. When a system is composed of diverse components, it is better able to withstand failures and recover from outages. This is because diverse systems are less vulnerable to single points of failure, and they can continue to function even when one component is compromised. By building diversity into IT systems, organizations can improve their resilience and reduce the risk of outages.",
        published_at=datetime(year=2025, month=12, day=1),
    ),
    News(
        id="16",
        source="false-negative",
        title="The lifecycle of insects",
        body="Insects go through a process called metamorphosis, in which they undergo a series of physical transformations as they develop from eggs to adults. During this process, insects are vulnerable to predators and environmental stressors. However, they have also developed remarkable strategies for survival and adaptation. In the world of software development, bugs can be thought of as a kind of metamorphosis. When a bug is introduced into a system, it can undergo a series of transformations as it is discovered, diagnosed, and debugged. During this process, the bug can cause significant problems for the system and its users. However, by developing effective strategies for bug detection and removal, developers can reduce the impact of bugs and improve the overall quality of their software.",
        published_at=datetime(year=2025, month=1, day=10),
    ),
]


def get_news() -> list[News]:
    """Return a list of fake news"""
    return [NEWS[randint(0, len(NEWS) - 1)]]
