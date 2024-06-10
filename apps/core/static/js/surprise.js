console.log(`
..............................°°°°°........
...........................................
............................°.°°°°°°°......
...........................°.°°°°°°.°......
.........°................°.°°°°°°°.°......
.......°°..°...............°°°°°°°.°.......
.........°..°°..........°.°°°°°°°°.°.......
.....°°°°°°°..°........°°.°°°°°°°°.°.......
.....°.°°°°°°°.°......°°.°°°°°°°°°.°.......
......°.°°°°°°°.°°....°.°°°°°°°°°°.°.......
......°.°°°°°°°°.°°..°.°°°°°°°°°°.°........
......°.°°°°°°°°°°.°°.°°°°°°°°°°°.°........
.......°.°°°°°°°°°°..°°°°°°°°°°°°.°........
.......°.°°°°°°°°°°°°°°°°°°°°°°°°.°........
........°.°°°°°°°°°°°°°°°°°°°°°°.°.........
........°.°°°°°°°°°°°°°°°°°°°°°°.°.........
........°.°°°°°°°°°°°°°°°°°°°°°°.°.........
.........°.°°°°°°°°°°°°°°°°°°°°°.°.........
.........°.°°°°°°°°°°°°°°°°°°°°°.°.........
..........°.°°°°°°°°°°°°°°°°°°°.°..........
..........°.°°°°°°°°°°°°°°°°°°°.°..........
..........°°°°°°°°°°°°°°°°°°°°°°°..........
...........................................
`);

console.log(`
OwO

Hey there!
What are you doing here?
did you know?
Unicorns are awesome
`);

let storyIndex = 0;
let originalTitle = document.title;

const titleStories = [
  "😴 Tab Inactive - Check out Vitary when you're back!",
  "😃 Hey there! Ready for some digital adventures?",
  "😳 Feeling curious? Explore and discover!",
  "😜 Ready to dazzle the digital realm?",
  "😌 Take a deep breath. What's on your mind?",
  "😇 Need a virtual hug? Vitary's got you covered!",
  "🎉 Let's make today a memorable one!",
  "😃 What's your story? Share it with Vitary!",
  "😎 Feeling cool? Vitary thinks so!",
  "🚀 Blast off into the wonders of Vitary!",
  "😊 Smile, it's a brand new digital day!",
  "🌈 Colors of creativity await your brush!",
  "😂 Laughter is the best pixel medicine!",
  "🔍 Seek and you shall find! What's next?",
  "😌 Relax, unwind, and enjoy the digital vibes.",
  "😏 Got a secret? Vitary loves a good mystery!",
  "🎶 Play your digital tune in the symphony of Vitary!",
  "🌐 Navigate through the vastness of possibilities!",
  "👀 Eyes wide open for the magic of Vitary!",
  "😍 Love in the air? Let Vitary be the cupid!",
  "🚪 Curiosity unlocked a new door in Vitary!",
  "🌟 Shine bright like the digital star you are!",
  "😊 Positivity is the key to the Vitary kingdom!",
  "🤔 Pondering? Let's explore the unknown!",
  "🌙 Nighttime whispers secrets to Vitary...",
  "😴 Sweet dreams, digital dreamer. See you soon!",
  "🌟 Just discovered a new corner of Vitary! It's like finding a hidden gem in the digital world. 💎✨",
  "😎 Feeling unstoppable today! What's your superpower in the digital realm? #DigitalHeroes",
  "🚀 Launched a poll to settle the great debate: Pineapple on pizza - yay or nay? Cast your votes! 🍍🍕 #PizzaWars",
  "🌈 Embracing the vibrant colors of creativity. Share your latest digital artwork with me! 🎨 #DigitalArt",
  "👀 Seeking recommendations for the next binge-worthy series. What's your current favorite show on the digital screen? 📺 #TVTime",
  "😂 Found myself in a GIF-off battle. Challenge accepted! Drop your funniest GIFs below. #GIFWar",
  "📸 Captured a moment that defines the essence of Vitary life. Share yours and let's create a digital scrapbook! #VitaryMoments",
  "🌐 Navigating the vastness of Vitary, one click at a time. What's your digital adventure for today? #ExploreVitary",
  "🤔 Contemplating the profound mysteries of the digital universe. Any existential thoughts to share? #DigitalPhilosophy",
  "🚪 Opened a door to a new digital dimension. What's behind your door of curiosity today? #CuriousVitary",
  "🎶 Creating a playlist for the Vitary community. Drop your favorite digital tunes below! 🎵 #VitaryJams",
  "👽 Discussing the possibility of extraterrestrial beings in the digital galaxy. What are your thoughts? 👾 #DigitalAliens",
  "🍔 Virtual lunchtime dilemma: Burrito or Burger? Cast your votes, and let's settle this digital debate! #FoodWars",
  "😇 Spreading digital kindness. Tag someone who deserves a virtual hug today! 🤗 #VitaryKindness",
  "🌌 Starry-eyed in the digital night. Share your favorite constellations with emojis! ✨🌙 #DigitalStargazing",
  "💭 Reflecting on the digital dreams that inspire us. What's your ultimate Vitary dream? #DreamBigVitary",
];

// If the document.hasFocus is false set the title to the story incremently by 2 sec
// setInterval(() => {
//   setInterval(function () {}, 10000);
//   if (!document.hasFocus()) {
//     document.title = titleStories[storyIndex];
//     storyIndex = (storyIndex + 1) % titleStories.length;
//   } else {
//     document.title = originalTitle;
//   }
// }, 2000);

// document.addEventListener("visibilitychange", () => {
//   document.title = originalTitle;
// });
