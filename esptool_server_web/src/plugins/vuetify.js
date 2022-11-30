import Vue from 'vue'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import '@mdi/font/css/materialdesignicons.css'
import zhHans from 'vuetify/lib/locale/zh-Hans'
import colors from 'vuetify/lib/util/colors'
Vue.use(Vuetify)

const opts = {}

export default new Vuetify({
    theme: {
        themes: {
            light: {
                primary: colors.deepPurple.accent4,
                secondary: colors.deepPurple.accent3,
                accent: colors.shades.black,
                error: colors.red.accent3,
            },
            dark: {
                primary: colors.blue.lighten3,
            },
        },
    },
    lang: {
        locales: { zhHans },
        current: 'zhHans',
    },
    icons: {
        iconfont: 'mdi', // 'mdi' || 'mdiSvg' || 'md' || 'fa' || 'fa4' || 'faSvg'
    },
})