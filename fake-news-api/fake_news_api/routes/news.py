from datetime import datetime

from fake_news_api.models.news import News

NEWS: list[News] = [
    News(
        source="hackernoon",
        title="The Rise of Ransomware Attacks",
        content="Ransomware attacks have become increasingly common in recent years, with hackers targeting businesses, governments, and individuals alike. These attacks involve encrypting sensitive data and demanding payment in exchange for the decryption key. The rise of ransomware attacks can be attributed to the growing use of cryptocurrencies, which provide a convenient and anonymous way for hackers to receive payments. To protect against ransomware attacks, it's essential to implement robust cybersecurity measures, including regular backups, software updates, and employee training.",
        posted_at=datetime(year=2025, month=1, day=1),
    ),
    News(
        source="google",
        title="Google Cloud Outage Causes Widespread Disruptions",
        content="A recent outage at Google Cloud caused disruptions to several popular services, including Gmail, Google Drive, and YouTube. The outage was attributed to a technical issue with Google's network infrastructure. The incident highlighted the importance of cloud infrastructure and the need for robust disaster recovery plans. Google apologized for the outage and promised to take steps to prevent similar incidents in the future.",
        posted_at=datetime(year=2025, month=2, day=4),
    ),
    News(
        source="yoga-society",
        title="The Benefits of Meditation for Mental Health",
        content="Meditation has long been recognized as a valuable tool for improving mental health. By reducing stress and anxiety, meditation can help individuals develop a greater sense of well-being and resilience. Regular meditation practice has also been shown to improve sleep quality, boost mood, and enhance cognitive function. With the growing demands of modern life, meditation provides a valuable opportunity for individuals to take a step back, relax, and recharge.",
        posted_at=datetime(year=2023, month=12, day=10),
    ),
    News(
        source="cyber-news",
        title="The Importance of Password Management",
        content="Password management is a critical aspect of cybersecurity, with weak passwords providing an easy entry point for hackers. To protect against password-related threats, it's essential to implement robust password management practices, including the use of unique, complex passwords and regular password updates. Password managers can also provide a convenient and secure way to store and generate passwords.",
        posted_at=datetime(year=2022, month=6, day=1),
    ),
    News(
        source="datacenter-world",
        title="Power Grid Failure Causes Widespread Blackouts",
        content="A recent power grid failure caused widespread blackouts across several states, leaving millions without electricity. The incident highlighted the importance of grid resilience and the need for robust infrastructure. Investigators attributed the failure to a combination of technical and human factors. Utility companies promised to take steps to prevent similar incidents in the future.",
        posted_at=datetime(year=2024, month=7, day=1),
    ),
    News(
        source="better-health",
        title="The Benefits of Regular Exercise for Physical Health",
        content="Regular exercise provides numerous benefits for physical health, including weight management, improved cardiovascular health, and enhanced muscle strength. Exercise also reduces the risk of chronic diseases, such as diabetes and certain types of cancer. With the growing demands of modern life, regular exercise provides a valuable opportunity for individuals to take care of their physical health.",
        posted_at=datetime(year=2022, month=2, day=2),
    ),
    News(
        source="cyberspace",
        title="The Rise of Phishing Attacks",
        content="Phishing attacks have become increasingly common in recent years, with hackers targeting businesses, governments, and individuals alike. These attacks involve tricking individuals into revealing sensitive information, such as login credentials or financial information. To protect against phishing attacks, it's essential to implement robust cybersecurity measures, including employee training and email filtering.",
        posted_at=datetime(year=2024, month=3, day=4),
    ),
    News(
        source="microsoft",
        title="Microsoft Azure Outage Causes Disruptions to Cloud Services",
        content="A recent outage at Microsoft Azure caused disruptions to several cloud services, including Azure Storage and Azure Virtual Machines. The outage was attributed to a technical issue with Microsoft's network infrastructure. The incident highlighted the importance of cloud infrastructure and the need for robust disaster recovery plans. Microsoft apologized for the outage and promised to take steps to prevent similar incidents in the future.",
        posted_at=datetime(year=2024, month=10, day=12),
    ),
    News(
        source="better-self",
        title="The Benefits of Mindfulness for Mental Health",
        content="Mindfulness has long been recognized as a valuable tool for improving mental health. By reducing stress and anxiety, mindfulness can help individuals develop a greater sense of well-being and resilience. Regular mindfulness practice has also been shown to improve sleep quality, boost mood, and enhance cognitive function. With the growing demands of modern life, mindfulness provides a valuable opportunity for individuals to take a step back, relax, and recharge.",
        posted_at=datetime(year=2024, month=2, day=2),
    ),
    News(
        source="cyber-world",
        title="The Importance of Software Updates",
        content="Software updates are a critical aspect of cybersecurity, with outdated software providing an easy entry point for hackers. To protect against software-related threats, it's essential to implement robust software update practices, including regular updates and patching. This can help prevent cyber attacks and protect sensitive data.",
        posted_at=datetime(year=2024, month=6, day=6),
    ),
]


def get_news() -> list[News]:
    """Return a list of fake news"""
    return NEWS
