/* ============================================================
   免费工具集成导航 - 数据文件
   结构: 一级分类 > 二级分类 > 工具条目
   ============================================================ */
window.TOOL_DATA = [

/* ========== 01 办公文档 ========== */
{
  id: "office", name: "办公文档", icon: "📄", color: "#4f7cff",
  groups: [
    {
      id: "ocr", name: "OCR 文字识别", icon: "🔍",
      tools: [
        { name: "Umi-OCR", url: "https://github.com/hiroi-sora/Umi-OCR", desc: "开源本地离线 OCR，批量识别、截图识别，完全免费无限制", tags: "开源,离线,批量", free: "完全免费" },
        { name: "白描 OCR", url: "https://web.baimiaoapp.com/", desc: "网页版文字识别，支持图片转文字、公式识别、表格识别", tags: "多语言,公式", free: "免费额度" },
        { name: "PEAROCR", url: "https://pearocr.com/", desc: "纯前端本地识别，图片不上传服务器，隐私最安全", tags: "本地处理,隐私", free: "完全免费" },
        { name: "CATOCR", url: "https://catocr.com/", desc: "轻量在线 OCR，支持多种图片格式，识别速度快", tags: "轻量,快速", free: "免费" },
        { name: "OCReditor", url: "https://ocreditor.com/", desc: "OCR 与文本编辑一体化，识别结果可直接编辑排版", tags: "编辑一体", free: "免费" },
        { name: "掌上识别王", url: "https://www.zhangshangshibie.com/", desc: "移动端优化的识别工具，支持拍照取字、证件识别", tags: "移动端,证件", free: "免费额度" },
        { name: "WEOCR", url: "https://ocr.plantree.me/", desc: "在线 OCR 服务，支持 PDF / 图片多种文档格式", tags: "PDF识别", free: "免费" },
        { name: "PDF24 OCR", url: "https://tools.pdf24.org/zh/ocr-pdf", desc: "PDF24 出品的 PDF 文字识别，德语服务器，隐私合规", tags: "PDF,无限量", free: "完全免费" },
        { name: "轻闪 OCR", url: "https://lightpdf.cn/ocr", desc: "批量图片转文字，支持导出 Word / Excel / TXT", tags: "批量,多格式导出", free: "免费额度" },
        { name: "TextIn 工具", url: "https://tools.textin.com/", desc: "专业级高精度 OCR，表格 / 票据 / 公式识别能力强", tags: "高精度,表格", free: "免费额度" },
        { name: "Excel OCR 识别", url: "https://toexcel.zhiyakeji.com/", desc: "表格图片直接还原为可编辑 Excel，结构保留好", tags: "表格还原", free: "免费额度" },
        { name: "微信读书 OCR 在线版", url: "https://ocr.wdku.net/", desc: "免费在线识别，支持中文/繁体/日韩/英法等，输出 PDF/Word/TXT", tags: "多语言,单次999张", free: "免费额度" },
        { name: "OnlineOCR.net", url: "https://www.onlineocr.net/", desc: "老牌在线 OCR，支持 PDF/JPG/PNG/TIFF 转 Word/Excel", tags: "老牌,多格式", free: "15页/小时" },
        { name: "NewOCR", url: "https://www.newocr.com/", desc: "免费在线 OCR，支持 100+ 语言，可上传或远程 URL", tags: "多语言", free: "15MB/文件" },
        { name: "飞桨 PaddleOCR", url: "https://openi.pcl.ac.cn/blt/PaddleOCR/releases", desc: "百度开源 OCR 引擎，本地部署，精度业界领先", tags: "开源,可部署", free: "完全免费" },
        { name: "Tesseract", url: "https://github.com/tesseract-ocr/tesseract", desc: "Google 开源 OCR 引擎，多语言包，可批处理自动化", tags: "开源,命令行", free: "完全免费" }
      ]
    },
    {
      id: "pdf", name: "PDF 工具", icon: "📕",
      tools: [
        { name: "PDF24 Tools", url: "https://tools.pdf24.org/zh/", desc: "40+ PDF 工具全集，无水印无次数限制，另有 Windows 客户端", tags: "全能,无限量,客户端", free: "完全免费" },
        { name: "iLovePDF", url: "https://www.ilovepdf.com/zh-cn", desc: "20+ 工具，合并拆分压缩转换，免登录即可用", tags: "全能,批量", free: "免费(有上限)" },
        { name: "PDF 派", url: "https://www.pdfpai.com/", desc: "国内访问快，PDF 转 Word/Excel/PPT/图片等全套功能", tags: "国内友好", free: "免费额度" },
        { name: "LuxPDF", url: "https://luxpdf.com/", desc: "开源全能 PDF 工具箱，15+ 功能，浏览器本地处理不上传", tags: "开源,本地处理", free: "完全免费" },
        { name: "PDFgear", url: "https://pdfgear.com/", desc: "无文件大小与次数限制，网页版+桌面端全功能编辑", tags: "无限制,客户端", free: "完全免费" },
        { name: "Stirling PDF", url: "https://stirlingpdf.io/?lang=zh_CN", desc: "开源可自建的 PDF 全家桶，隐私优先，功能极全", tags: "开源,可自建", free: "完全免费" },
        { name: "Smallpdf", url: "https://smallpdf.com/cn", desc: "界面最美观的 PDF 工具，操作简单直观", tags: "UI优秀", free: "2次/天" },
        { name: "CleverPDF", url: "https://www.cleverpdf.com/cn", desc: "30+ PDF 转换工具，支持批量处理与格式互转", tags: "转换全", free: "免费额度" },
        { name: "轻闪 PDF", url: "https://lightpdf.cn/", desc: "轻量 PDF 工具集，转换、编辑、OCR、签名一站搞定", tags: "轻量,含OCR", free: "免费额度" },
        { name: "Sejda PDF", url: "https://www.sejda.com/", desc: "可直接编辑 PDF 内文字与图片，界面清爽无干扰", tags: "编辑文字", free: "3次/小时" },
        { name: "Xodo PDF", url: "https://xodo.com/", desc: "最佳免费 PDF 批注与电子签名工具，支持协作", tags: "批注,签名", free: "完全免费" },
        { name: "GoToPDF", url: "https://gotopdf.net/", desc: "浏览器本地处理（pdf-lib），文件不上传，无限制", tags: "本地处理,无限制", free: "完全免费" },
        { name: "docsmall", url: "https://docsmall.com/", desc: "PDF 压缩、合并、分割、图片压缩，国内访问快", tags: "压缩强", free: "免费额度" },
        { name: "PDF 图片提取", url: "https://www.extractpdf.com/zh.html", desc: "一键从 PDF 中提取所有内嵌图片，保留原始质量", tags: "提取图片", free: "完全免费" },
        { name: "PDFsam", url: "https://pdfsam.org/zh/", desc: "开源 PDF 分割合并工具，另有桌面客户端", tags: "开源,分割合并", free: "完全免费" },
        { name: "转转大师", url: "https://pdftoword.55.la/", desc: "PDF 与 Word 高保真互转，排版保留好", tags: "PDF转Word", free: "免费额度" },
        { name: "超级 PDF", url: "https://xpdf.cn/", desc: "国内老牌 PDF 处理站，转换/压缩/加密功能齐", tags: "国内老牌", free: "免费额度" },
        { name: "Right PDF", url: "https://online.rightpdf.com/cn/home", desc: "精准 PDF 处理，格式转换与版面还原准确", tags: "精准转换", free: "免费额度" },
        { name: "CAJ 转 PDF", url: "https://caj2pdf.cn/", desc: "知网 CAJ 格式在线转 PDF，学术党必备", tags: "CAJ转换", free: "免费额度" },
        { name: "CloudConvert", url: "https://cloudconvert.com/", desc: "云端万能格式转换，支持 200+ 文件格式", tags: "万能转换", free: "25次/天" },
        { name: "PDF Candy", url: "https://pdfcandy.com/cn/pdf-ocr.html", desc: "47 个免费 PDF 工具，含 OCR、图片提取、加密等", tags: "工具多,含OCR", free: "免费额度" },
        { name: "万兴 PDF", url: "https://www.hipdf.cn/", desc: "专业 PDF 编辑与转换，支持批量处理", tags: "专业级", free: "免费额度" }
      ]
    },
    {
      id: "ppt-tpl", name: "PPT 模板资源", icon: "🎨",
      tools: [
        { name: "Office PLUS", url: "https://www.officeplus.cn/PPT/template/", desc: "微软官方模板站，全部免费无水印无广告，商务校园全覆盖", tags: "官方,无水印", free: "完全免费" },
        { name: "第一 PPT", url: "https://www.1ppt.com/", desc: "2005 年老牌站，无需注册即可下载，课件资源最丰富", tags: "老牌,免注册", free: "完全免费" },
        { name: "优品 PPT", url: "https://www.ypppt.com/", desc: "简约清新风，毕业答辩/简历/年终总结模板全免费", tags: "简约风,全免费", free: "完全免费" },
        { name: "51PPT 模板网", url: "https://www.51pptmoban.com/", desc: "号称百万模板，纯免费不用登录直接下载", tags: "量大,免登录", free: "完全免费" },
        { name: "PPT 世界", url: "https://www.pptx.cn/", desc: "设计师作品社区，设计感强、更新快，支持多格式下载", tags: "设计感,更新快", free: "免费社区" },
        { name: "PPT 超级市场", url: "https://www.pptsupermarket.com/ppts/", desc: "模板+文案+教程一体，配现成文案，多数模板免费", tags: "含文案", free: "多数免费" },
        { name: "PPT 家园", url: "https://www.pptjia.com/", desc: "国内老牌模板站，分类清晰，免费模板储备充足", tags: "老牌,分类全", free: "免费为主" },
        { name: "HIPPTer 导航", url: "https://www.hippter.com/", desc: "PPT 资源导航站，聚合素材/模板/图表/配色工具", tags: "导航聚合", free: "免费导航" },
        { name: "吾道幻灯片", url: "https://www.woodo.cn/design/template/", desc: "在线协作幻灯片，模板可在线编辑后导出", tags: "在线编辑", free: "免费额度" },
        { name: "稻壳儿 WPS", url: "https://www.docer.com/", desc: "WPS 内置模板商城，筛选「免费」标签即可零付费", tags: "WPS内置", free: "免费专区" },
        { name: "站长素材 PPT", url: "https://sc.chinaz.com/ppt/", desc: "站长之家旗下，PPT 模板/背景/图表素材丰富", tags: "素材全", free: "免费为主" },
        { name: "办公资源网", url: "https://www.bangongziyuan.com/", desc: "PPT/Word/Excel 模板综合站，海量免费办公模板", tags: "办公综合", free: "免费额度" },
        { name: "PPT 宝藏", url: "https://www.pptbz.com/", desc: "老牌资源社区，中国风/教育/医疗等细分风格全", tags: "风格细分", free: "金币制" },
        { name: "Slidesgo", url: "https://slidesgo.com/", desc: "国外高质量模板站，设计现代，Google Slides + PPT 双格式", tags: "国外,设计佳", free: "免费+署名" },
        { name: "Canva 模板", url: "https://www.canva.cn/templates/", desc: "海量在线设计模板，PPT 可在线编辑直接导出", tags: "在线设计", free: "免费专区" }
      ]
    },
    {
      id: "aippt", name: "AI 生成 PPT", icon: "🤖",
      tools: [
        { name: "Kimi PPT", url: "https://www.kimi.com/", desc: "月之暗面出品，长文本解析强，一句话生成整套 PPT", tags: "长文本,国内", free: "免费额度" },
        { name: "AiPPT.cn", url: "https://www.aippt.cn/", desc: "输入主题即出大纲与成稿，中文模板库大", tags: "中文模板多", free: "免费额度" },
        { name: "WPS AI", url: "https://ai.wps.cn/", desc: "WPS 内置 AI，不跳出办公套件，中文排版优秀", tags: "WPS内置", free: "免费额度" },
        { name: "MindShow", url: "https://www.mindshow.fun/", desc: "Markdown / 大纲一键转 PPT，逻辑结构清晰", tags: "大纲转PPT", free: "免费额度" },
        { name: "轻竹办公", url: "https://www.qzoffice.com/", desc: "AI 生成 PPT + 文档，中文排版稳，导出无水印", tags: "导出无水印", free: "免费额度" },
        { name: "ChatPPT", url: "https://www.chat-ppt.com/", desc: "对话式生成 PPT，边聊边改，支持一键换肤", tags: "对话式", free: "免费额度" },
        { name: "笔灵 PPT", url: "https://ibiling.cn/ppt-zone", desc: "AI 写大纲+生成 PPT，公文与汇报场景适配好", tags: "公文汇报", free: "免费额度" },
        { name: "iSlide", url: "https://www.islide.cc/", desc: "PPT 设计插件+AI 生成，海量图表与图标素材", tags: "插件+素材", free: "免费额度" },
        { name: "歌者 PPT", url: "https://gezhe.com/", desc: "AI 生成 PPT，支持导入文档自动成稿", tags: "文档成稿", free: "免费额度" },
        { name: "Gamma", url: "https://gamma.app/", desc: "国外最热门 AI PPT，设计感第一梯队，10 秒出稿", tags: "设计感强", free: "400额度/月" },
        { name: "讯飞智文", url: "https://zhiwen.xfyun.cn/", desc: "科大讯飞出品，免费无水印，语音转 PPT 是独门绝技", tags: "无水印,语音转PPT", free: "免费额度" },
        { name: "百度文库 AI", url: "https://wenku.baidu.com/", desc: "上传多格式文档生成 PPT，中文排版优秀", tags: "多格式输入", free: "免费额度" },
        { name: "美图 AI PPT", url: "https://www.designkit.com/", desc: "美图出品，颜值高，模板丰富适合对外展示", tags: "颜值高", free: "免费额度" },
        { name: "爱设计 PPT", url: "https://ppt.isheji.com/", desc: "在线设计+AI 生成，模板与素材库丰富", tags: "在线设计", free: "免费额度" },
        { name: "职得 PPT", url: "https://www.lgppt.cn/", desc: "面向职场汇报的 AI PPT 生成工具", tags: "职场汇报", free: "免费额度" }
      ]
    },
    {
      id: "wemp", name: "公众号图文编辑", icon: "📱",
      tools: [
        { name: "微信公众平台", url: "https://mp.weixin.qq.com/", desc: "官方后台，素材管理与图文编辑的起点", tags: "官方", free: "完全免费" },
        { name: "135 编辑器", url: "https://www.135editor.com/beautify_editor.html", desc: "公众号排版老牌工具，样式库最大，一键同步微信", tags: "样式最全", free: "免费版够用" },
        { name: "96 微信编辑器", url: "https://bj.96weixin.com/", desc: "模板丰富，支持一键排版、图片素材库、SVG 互动", tags: "模板多", free: "免费版够用" },
        { name: "秀米 XIUMI", url: "https://xiumi.us/", desc: "排版设计感强，H5 制作优秀，视觉党首选", tags: "设计感强,含H5", free: "免费版够用" },
        { name: "稿定设计", url: "https://www.gaoding.com/", desc: "在线设计+公众号配图，封面图/海报/长图一站搞定", tags: "配图设计", free: "免费额度" },
        { name: "创客贴", url: "https://www.chuangkit.com/", desc: "公众号封面、配图、海报在线设计，模板海量", tags: "封面配图", free: "免费额度" },
        { name: "Canva 可画", url: "https://www.canva.cn/", desc: "国际设计平台中文版，公众号图文+封面+视频封面", tags: "全能设计", free: "免费版够用" },
        { name: "壹伴编辑器", url: "https://yiban.io/", desc: "浏览器插件式公众号助手，采集图文、一键排版", tags: "插件,采集", free: "免费版" },
        { name: "Fotor 懒设计", url: "https://www.fotor.com.cn/", desc: "公众号配图与图片美化，AI 抠图/改图", tags: "图片美化", free: "免费额度" }
      ]
    }
  ]
},

/* ========== 02 影音娱乐 ========== */
{
  id: "media", name: "影音娱乐", icon: "🎬", color: "#ff5c8a",
  groups: [
    {
      id: "m3u8", name: "M3U8 影视资源站", icon: "🎞️",
      tools: [
        { name: "卧龙资源", url: "https://wolongzyw.com/", desc: "26 路片源，无防盗链，采集稳定老牌资源站", tags: "26路,无防盗链", free: "免费采集" },
        { name: "光速资源", url: "https://www.guangsuzy.com/", desc: "16 路 m3u8 直链，国内 CDN，高峰略慢", tags: "16路,国内CDN", free: "免费采集", api: "https://api.guangsuapi.com/api.php/provide/vod/from/gsm3u8" },
        { name: "闪电资源", url: "https://shandianzy.cc/", desc: "20 路片源，更新快；接口仅支持列表浏览，不支持关键词搜索", tags: "20路,更新快", free: "免费采集", api: "http://sdzyapi.com/api.php/provide/vod/from/sdm3u8", nosearch: true },
        { name: "量子资源", url: "https://cj.lziapi.com/", desc: "88 路片源，稳定性业界公认，采集首选之一", tags: "88路,最稳定", free: "免费采集", api: "https://cj.lziapi.com/api.php/provide/vod" },
        { name: "红牛资源", url: "https://www.hongniuzy.com/", desc: "老牌资源站，国内速度优、更新快", tags: "老牌,国内快", free: "免费采集", api: "https://hongniuzy2.com/api.php/provide/vod/from/hnm3u8" },
        { name: "无尽资源", url: "http://www.wujinzy.net/", desc: "速度一般但片源较全；接口被 Cloudflare 防护，仅支持站内搜索", tags: "片源全", free: "免费采集" },
        { name: "360 资源", url: "https://360zyzz.com/", desc: "57 路片源，偶发 403，备用资源站", tags: "57路,备用", free: "免费采集", api: "https://360zyzz.com/api.php/provide/vod" },
        { name: "樱花资源", url: "https://yhzy.cc/", desc: "m3u8 直链接口，日韩剧集覆盖较好；接口已限制外站调用", tags: "m3u8直链", free: "免费采集" },
        { name: "最大资源", url: "http://zuida001.com/", desc: "老牌资源站，片源库庞大，接口稳定", tags: "老牌,片源多", free: "免费采集", api: "https://api.zuidapi.com/api.php/provide/vod" },
        { name: "爱奇艺资源站", url: "https://iqiyizy1.com/", desc: "国内 CDN 加速秒拖秒播，热剧首发，1080P 超清", tags: "热剧快,1080P", free: "免费采集", api: "https://iqiyizyapi.com/api.php/provide/vod" },
        { name: "金鹰资源", url: "http://jinyingzy.com/", desc: "29 路片源，低延迟国内 CDN 秒拖秒播", tags: "29路,低延迟", free: "免费采集", api: "http://jyzyapi.com/provide/vod/from/jinyingm3u8" },
        { name: "天涯影视资源", url: "https://tyyszy5.com/", desc: "支持 JSON/XML 双接口；接口暂不支持关键词搜索，可站内浏览", tags: "双接口", free: "免费采集", api: "https://tyyszyapi.com/api.php/provide/vod", nosearch: true },
        { name: "无水印资源", url: "https://www.wsyzy.top/", desc: "无水印影视资源，含电影/电视剧/动漫；接口暂不支持关键词搜索", tags: "无水印", free: "免费采集", api: "https://api.wsyzy.net/api.php/provide/vod/from/wsym3u8", nosearch: true },
        { name: "华为吧资源", url: "https://huaweiba.live/", desc: "新片上线较快，m3u8 直链资源站", tags: "新片快", free: "免费采集" },
        { name: "索尼资源", url: "https://suonizy.net/", desc: "片源质量较好，适合作为补充采集源", tags: "补充源", free: "免费采集" },
        { name: "OK 资源", url: "https://okzyw.cc/", desc: "综合影视资源站，备用采集源", tags: "综合,备用", free: "免费采集" },
        { name: "豆瓣资源站", url: "https://dbzy.tv", desc: "广告主资源站，国内 CDN 加速实时秒播", tags: "国内CDN,秒播", free: "免费采集" },
        { name: "U 酷资源站", url: "https://ukuzy0.com/", desc: "最新片源，商业 CDN 加速，播放流畅", tags: "最新片源", free: "免费采集" },
        { name: "快车资源站", url: "http://kuaichezy.com/", desc: "HTTPS 资源，m3u8 直链，稳定采集源", tags: "m3u8直链", free: "免费采集" },
        { name: "CK 资源站", url: "http://www.ckzy1.com/", desc: "HTTPS 资源，带跑马灯广告，备用采集源", tags: "备用源", free: "免费采集" },
        { name: "飞牛影视资源合集", url: "https://club.fnnas.com/forum.php?mod=viewthread&tid=48467", desc: "NAS 社区整理的标准化接口清单，含大量可用资源站 API", tags: "接口清单", free: "免费" }
      ]
    },
    {
      id: "music-dl", name: "音乐下载工具", icon: "🎵",
      tools: [
        { name: "下歌吧", url: "https://xiageba.com/", desc: "老牌音乐下载站，支持多平台歌曲搜索与下载", tags: "老牌,多平台", free: "免费" },
        { name: "歌曲宝", url: "https://www.gequbao.com/", desc: "在线试听+下载，曲库更新较快，界面清爽", tags: "曲库全", free: "免费" },
        { name: "HIFIHI", url: "https://www.hifihi.com/", desc: "高音质音乐搜索下载，支持无损音质", tags: "无损音质", free: "免费" },
        { name: "音乐搜索器", url: "https://music.itzo.cn/a.php", desc: "聚合多平台音乐搜索，一个入口搜全网", tags: "聚合搜索", free: "免费" },
        { name: "全网免费音乐", url: "https://iui.su/2217/", desc: "整理的免费音乐资源导航合集，含多个可用站点", tags: "资源合集", free: "免费" }
      ]
    },
    {
      id: "ai-music", name: "AI 音乐创作", icon: "🎼",
      tools: [
        { name: "Suno", url: "https://suno.com/", desc: "全球最强 AI 音乐生成，输入歌词即出完整人声歌曲，v6 结构/人声最自然", tags: "最强,全曲人声", free: "免费额度" },
        { name: "苏诺音乐 Suno.cn", url: "https://suno.cn/", desc: "Suno 中文站点，中文界面与中文歌词优化，国内可访问", tags: "中文版,国内可用", free: "免费额度" },
        { name: "Udio", url: "https://www.udio.com/", desc: "原始音频保真度最强，原声乐器与爵士古典细节出色", tags: "高保真,器乐强", free: "免费额度" },
        { name: "AIVA", url: "https://www.aiva.ai/", desc: "古典/影视配乐专长，支持 MIDI 导出，作曲工作流完整", tags: "配乐,MIDI导出", free: "免费额度" },
        { name: "Soundraw", url: "https://soundraw.io/", desc: "免版税背景音乐生成，可商用授权清晰，视频/Podcast 首选", tags: "可商用,免版税", free: "免费试听" },
        { name: "Mubert", url: "https://mubert.com/", desc: "自适应音乐与 API 生成为主，适合 App 与直播场景", tags: "API,自适应", free: "免费额度" },
        { name: "Beatoven.ai", url: "https://www.beatoven.ai/", desc: "情绪场景化配乐生成，价格亲民，适合短视频", tags: "场景配乐,便宜", free: "免费额度" },
        { name: "Boomy", url: "https://boomy.com/", desc: "极简上手，几秒生成可发布曲目，适合快速试错", tags: "极简,可发布", free: "免费额度" },
        { name: "YuE 开源模型", url: "https://github.com/multimodal-art-projection/YuE", desc: "唯一支持真实歌词的开源歌声生成模型，可本地部署", tags: "开源,可本地", free: "完全免费" },
        { name: "DeepSeek 作词", url: "https://chat.deepseek.com/", desc: "AI 歌词创作与改写助手，为 Suno/Udio 提供歌词素材", tags: "作词辅助", free: "完全免费" },
        { name: "歌词改编大师", url: "https://www.coze.cn/store/agent/7362335983632760871", desc: "扣子智能体，专门针对 Suno 歌词做改编与结构化", tags: "歌词改编", free: "免费额度" },
        { name: "歌词创作专家", url: "https://www.coze.cn/store/agent/7359503215928573993", desc: "扣子智能体，按风格与主题生成可直投 Suno 的歌词", tags: "歌词生成", free: "免费额度" },
        { name: "歌词生成专家", url: "https://www.coze.cn/store/agent/7363557725072031754", desc: "扣子智能体，快速产出押韵规整的成篇歌词", tags: "快速成篇", free: "免费额度" },
        { name: "音核原创", url: "http://bbs.zhu-zi.com/forum-29-482.html", desc: "专业歌词创作交流社区，可找人合作作词作曲", tags: "社区交流", free: "免费" },
        { name: "中国原创歌词网", url: "https://www.zgycgc.com/", desc: "中国原创歌词创作平台，海量原创歌词可参考", tags: "歌词库", free: "免费" },
        { name: "原创作词网", url: "http://www.zuoci.net/", desc: "原创歌词创作与分享平台", tags: "歌词库", free: "免费" },
        { name: "歌词网", url: "http://www.gecicn.com/index.htm", desc: "歌词创作与欣赏平台，含大量成品歌词参考", tags: "歌词参考", free: "免费" }
      ]
    },
    {
      id: "video-creator", name: "视频分发 · 创作者平台", icon: "📹",
      tools: [
        { name: "抖音创作者中心", url: "https://creator.douyin.com/", desc: "抖音官方面向创作者的发布、数据中心、活动与创作工具入口", tags: "短视频,数据后台", free: "免费" },
        { name: "微信视频号助手", url: "https://channels.weixin.qq.com/index", desc: "视频号官方发布后台，支持直播、动态与数据中心", tags: "视频号,官方", free: "免费" },
        { name: "哔哩哔哩创作中心", url: "https://member.bilibili.com/platform/home", desc: "B 站投稿/数据/激励/粉丝管理后台，UP 主必备", tags: "中长视频,官方", free: "免费" },
        { name: "快手创作者平台", url: "https://cp.kuaishou.com/profile", desc: "快手官方创作者中心，作品发布、直播、数据与变现", tags: "短视频,官方", free: "免费" },
        { name: "西瓜视频创作中心", url: "https://studio.ixigua.com/", desc: "字节系中视频平台官方后台，与抖音联动分发", tags: "中视频,官方", free: "免费" },
        { name: "好看视频创作平台", url: "https://dream.haokan.com/author/upload", desc: "百度旗下视频平台创作中心，搜索流量分发优势", tags: "百度系,官方", free: "免费" },
        { name: "腾讯视频创作平台", url: "https://mp.v.qq.com/manage/0", desc: "腾讯视频 MP 平台，长视频与短视频投稿后台", tags: "长视频,官方", free: "免费" },
        { name: "优酷开放平台", url: "https://mp.youku.com/new/video", desc: "优酷创作者后台，视频上传与分成体系", tags: "长视频,官方", free: "免费" },
        { name: "爱奇艺号", url: "https://mp.iqiyi.com/ccenter/publish", desc: "爱奇艺自媒体发布平台，影视内容与分账合作", tags: "长视频,分账", free: "免费" },
        { name: "AcFun 创作中心", url: "https://member.acfun.cn/", desc: "A 站官方投稿与数据后台，二次元内容社区", tags: "二次元,官方", free: "免费" },
        { name: "百家号", url: "https://baijiahao.baidu.com/", desc: "百度内容分发平台，图文+视频，搜索流量强", tags: "图文+视频", free: "免费" },
        { name: "腾讯微视", url: "https://media.weishi.qq.com/", desc: "腾讯短视频平台媒体后台", tags: "短视频,官方", free: "免费" }
      ]
    }
  ]
},

/* ========== 03 资讯查询 ========== */
{
  id: "info", name: "资讯查询", icon: "📰", color: "#12b886",
  groups: [
    {
      id: "news", name: "国际新闻导航", icon: "🌍",
      tools: [
        { name: "观察者网", url: "https://www.guancha.cn/", desc: "国际时政深度报道与评论，国内视角看世界", tags: "时政,评论", free: "免费" },
        { name: "环球网", url: "https://www.huanqiu.com/", desc: "环球时报旗下，国际新闻与军事资讯聚合", tags: "国际,军事", free: "免费" },
        { name: "龙腾网", url: "https://www.ltaaa.cn/", desc: "翻译海外网友评论，看外国人如何议论中国与世界", tags: "外网翻译", free: "免费" },
        { name: "金十数据", url: "https://www.jin10.com/", desc: "全球财经快讯实时直播，国际市场动向第一时间", tags: "财经快讯", free: "免费" },
        { name: "澎湃新闻", url: "https://www.thepaper.cn/", desc: "时政思想类深度报道，国际栏目质量高", tags: "深度报道", free: "免费" },
        { name: "腾讯新闻国际", url: "https://news.qq.com/ch/world/", desc: "腾讯国际新闻频道，资讯更新快覆盖面广", tags: "综合", free: "免费" },
        { name: "新华网国际", url: "http://www.news.cn/world/index.html", desc: "新华社国际频道，权威官方新闻源", tags: "权威官方", free: "免费" },
        { name: "新浪国际", url: "https://news.sina.com.cn/world/", desc: "新浪国际新闻，聚合多家媒体资讯", tags: "聚合", free: "免费" },
        { name: "网易国际", url: "https://news.163.com/world/", desc: "网易国际新闻频道，跟帖讨论活跃", tags: "综合", free: "免费" },
        { name: "中国网国际", url: "http://news.china.com.cn/node_7247303.htm", desc: "中国网国际频道，对外传播视角", tags: "官方", free: "免费" },
        { name: "中国新闻网国际", url: "https://www.chinanews.com.cn/world/", desc: "中新社国际新闻，华侨华人资讯特色", tags: "中新社", free: "免费" },
        { name: "参考消息", url: "https://www.cankaoxiaoxi.com/", desc: "翻译外媒报道，国际舆论风向标", tags: "外媒翻译", free: "免费" },
        { name: "澎湃国际", url: "https://www.thepaper.cn/channel_122908", desc: "澎湃新闻国际频道专题", tags: "专题", free: "免费" }
      ]
    },
    {
      id: "hot", name: "排行 · 热点聚合", icon: "🔥",
      tools: [
        { name: "今日热榜 TopHub", url: "https://tophub.today/", desc: "聚合全网主流平台热点排行榜，一站式追踪每日热门", tags: "全平台聚合", free: "完全免费" },
        { name: "即时热点", url: "https://nowhots.com/", desc: "实时追踪突发新闻与热门事件，热度飙升榜", tags: "实时突发", free: "完全免费" },
        { name: "微博热搜", url: "https://s.weibo.com/top/summary?cate=realtimehot", desc: "中文社交媒体风向标，实时热搜榜", tags: "社交风向", free: "完全免费" },
        { name: "百度热搜", url: "https://top.baidu.com/board?tab=realtime", desc: "基于海量搜索数据反映网民关注焦点", tags: "搜索趋势", free: "完全免费" },
        { name: "抖音热榜", url: "https://tophub.today/n/DpQvNABoNE", desc: "抖音热点榜聚合，掌握短视频平台最新动态", tags: "短视频", free: "完全免费" },
        { name: "知乎热榜", url: "https://www.zhihu.com/hot", desc: "中文问答社区热榜，话题讨论深度高", tags: "问答社区", free: "完全免费" },
        { name: "B 站热门榜", url: "https://www.bilibili.com/v/popular/rank/all", desc: "B 站全站排行榜，了解中长视频流行趋势", tags: "中长视频", free: "完全免费" },
        { name: "AnyKnew 新闻聚合", url: "https://www.anyknew.com/", desc: "一站聚合各大新闻平台热榜，纯净无广告", tags: "新闻聚合", free: "完全免费" },
        { name: "百度指数", url: "https://index.baidu.com/", desc: "关键词搜索热度趋势分析，看话题涨落", tags: "趋势分析", free: "免费额度" },
        { name: "微信指数", url: "https://weixin.qq.com/", desc: "微信生态内关键词热度趋势（搜一搜内查看）", tags: "微信生态", free: "完全免费" }
      ]
    },
    {
      id: "company", name: "企业查询工具", icon: "🏢",
      tools: [
        { name: "国家企业信用信息公示系统", url: "https://www.gsxt.gov.cn/index.html", desc: "市场监管总局官方数据，最权威的企业登记信息来源", tags: "官方,最权威", free: "完全免费" },
        { name: "企查查", url: "https://www.qcc.com/", desc: "企业工商、司法、知识产权、招投标信息最全", tags: "数据最全", free: "免费额度" },
        { name: "天眼查", url: "https://www.tianyancha.com/", desc: "企业关系图谱与风险监测，商业调查常用", tags: "关系图谱", free: "免费额度" },
        { name: "爱企查", url: "https://aiqicha.baidu.com/", desc: "百度旗下企业信息查询，免注册查看基础信息", tags: "百度,免注册", free: "免费为主" },
        { name: "企信宝", url: "https://www.qixin.com/", desc: "企业信用信息查询与信用评级", tags: "信用评级", free: "免费额度" },
        { name: "水滴信用", url: "https://shuidi.cn/", desc: "企业信用服务平台，含风险预警与失信名单", tags: "信用服务", free: "免费额度" },
        { name: "企洞察", url: "https://www.qidongcha.com/", desc: "企业信息深度查询，股权穿透与实控人分析", tags: "股权穿透", free: "免费额度" },
        { name: "番番寻客宝", url: "https://xunkebao.baidu.com/", desc: "百度旗下客户资源挖掘工具，找潜在客户线索", tags: "客户挖掘", free: "免费额度" },
        { name: "国家知识产权局", url: "https://pss-system.cponline.cnipa.gov.cn/", desc: "官方专利与商标检索系统，查专利法律状态", tags: "官方,专利商标", free: "完全免费" },
        { name: "中国裁判文书网", url: "https://wenshu.court.gov.cn/", desc: "最高法官方文书公开平台，查涉诉情况", tags: "官方,涉诉", free: "完全免费" },
        { name: "中国执行信息公开网", url: "http://zxgk.court.gov.cn/", desc: "官方查询失信被执行人、限制消费人员名单", tags: "官方,失信名单", free: "完全免费" },
        { name: "小微企业名录", url: "https://xwqy.gsxt.gov.cn/", desc: "市场监管总局小微企业认定与查询", tags: "官方,小微企业", free: "完全免费" }
      ]
    }
  ]
},

/* ========== 04 效率与美化 ========== */
{
  id: "utility", name: "效率与美化", icon: "✨", color: "#9b6bff",
  groups: [
    {
      id: "browser-ext", name: "插件下载站", icon: "🧩",
      tools: [
        { name: "Crx 搜搜", url: "https://crxsoso.com/", desc: "库量最大，收录 22 万+ Chrome 扩展 + Edge/Firefox，支持历史版本", tags: "库量最大,多平台", free: "完全免费" },
        { name: "极简插件", url: "https://chrome.zzzmh.cn/", desc: "界面最干净无广告，人工筛选收录，直达 crx 下载", tags: "干净,人工筛选", free: "完全免费" },
        { name: "画夹插件网", url: "https://huajiakeji.com/", desc: "更新最快，新上架扩展很快收录，含旧版本适配", tags: "更新最快", free: "完全免费" },
        { name: "插件小屋", url: "https://chajianxw.com/", desc: "分类最细，除常规类目还有健康/旅游/汽车等生活类", tags: "分类最细", free: "完全免费" },
        { name: "Chrome 插件网", url: "https://www.cnplugins.com/", desc: "国内老牌插件站，中文介绍详细，分类清晰", tags: "老牌,中文介绍", free: "完全免费" },
        { name: "Crx4Chrome", url: "https://www.crx4chrome.com/", desc: "国外镜像站，版本跟得最紧，需用英文名搜索", tags: "版本最新", free: "完全免费" },
        { name: "Edge 外接程序商店", url: "https://microsoftedge.microsoft.com/addons/", desc: "微软官方扩展商店，国内可直连，与 Chrome 扩展高度重合", tags: "官方,国内直连", free: "完全免费" },
        { name: "Firefox 扩展商店", url: "https://addons.mozilla.org/zh-CN/", desc: "火狐官方扩展库，国内可直连访问", tags: "官方,火狐", free: "完全免费" },
        { name: "360 浏览器扩展中心", url: "https://ext.se.360.cn/", desc: "360 安全浏览器官方扩展市场，含大量国内常用插件", tags: "官方,国内插件", free: "完全免费" },
        { name: "GitHub 扩展发布页", url: "https://github.com/search?q=chrome+extension&type=repositories", desc: "在 GitHub 直接搜扩展项目，最新开发版常在此发布", tags: "源码,最新版", free: "完全免费" }
      ]
    },
    {
      id: "ext-pick", name: "常用插件推荐", icon: "⭐",
      tools: [
        { name: "Tampermonkey 篡改猴", url: "https://chrome.zzzmh.cn/info/dhdgffkkebhmkfjojejmpbldmpobfkfo", desc: "用户脚本管理器，装脚本必备，浏览器扩展使用率常年第一", tags: "必备,脚本管理", free: "完全免费" },
        { name: "沉浸式翻译", url: "https://chrome.zzzmh.cn/info/bpoadfkcbjbfhfodiogcnhhhpibjhbnh", desc: "双语对照网页翻译，支持 PDF/EPUB/视频字幕，体验极佳", tags: "必备,双语对照", free: "完全免费" },
        { name: "Adblock", url: "https://chrome.zzzmh.cn/info/gighmmpiobklfepjocnamgkkbiglidom", desc: "经典广告拦截扩展，安装量最高的拦截工具之一", tags: "必备,广告拦截", free: "完全免费" },
        { name: "浮图秀", url: "https://chrome.zzzmh.cn/info/mgpdnhlllbpncjpgokgfogidhoegebod", desc: "鼠标悬停自动放大网页缩略图，看图神器", tags: "看图,悬停放大", free: "完全免费" },
        { name: "图片助手", url: "https://chrome.zzzmh.cn/info/dbjbempljhcmhlfpfacalomonjpalpko", desc: "一键提取当前网页全部图片，支持筛选与批量下载", tags: "图片提取,批量下载", free: "完全免费" },
        { name: "猫抓", url: "https://chrome.zzzmh.cn/info/jfedfbgedapdagkghmgibemcoggfppbb", desc: "嗅探网页视频/音频资源，m3u8 与媒体文件一键抓取", tags: "媒体嗅探,m3u8", free: "完全免费" },
        { name: "FireShot 截屏", url: "https://chrome.zzzmh.cn/info/mcbpblocgmgfnpjjppndjkmgjaogfceg", desc: "整页滚动截屏与编辑标注，支持导出 PDF", tags: "截图,滚动截屏", free: "完全免费" },
        { name: "SuperCopy 超级复制", url: "https://chrome.zzzmh.cn/info/onepmapfbjohnegdmfhndpefjkppbjkm", desc: "破解网页复制限制与右键禁用，文档网站常备", tags: "破解复制,解除限制", free: "完全免费" },
        { name: "腾讯翻译君", url: "https://chrome.zzzmh.cn/info/lkjkfecdnfjopaeaibboihfkmhdjmanm", desc: "腾讯出品划词翻译扩展，国内服务稳定", tags: "划词翻译", free: "完全免费" },
        { name: "谷歌翻译", url: "https://chrome.zzzmh.cn/info/fjkpgkefceopkogemcjcnncdhbgldolm", desc: "Google 官方翻译扩展，整页翻译与划词翻译", tags: "整页翻译", free: "完全免费" },
        { name: "快识图 OCR", url: "https://chrome.zzzmh.cn/info/oefooeopdahbeimdgamlblnpegijmdem", desc: "浏览器内直接对图片取字，截图即识别", tags: "OCR,截图取字", free: "完全免费" },
        { name: "极客侧边栏", url: "https://chrome.zzzmh.cn/info/gjkfnalkblnjkalnipilmaacibikciin", desc: "把 ChatGPT 等 AI 收纳进侧边栏，随时呼出", tags: "AI侧边栏,快捷", free: "完全免费" },
        { name: "一键读图", url: "https://ext.se.360.cn/#/extension-detail?id=hggdeafckfnnjmkpkhaikpkfhognldih", desc: "快速查看与保存网页图片，360 扩展中心版本", tags: "看图,保存图片", free: "完全免费" },
        { name: "vtool.pro 视频号下载", url: "https://vtool.pro/webstore.html", desc: "浏览器扩展形式的视频号视频下载工具", tags: "视频号,下载", free: "完全免费" },
        { name: "Jego 无忧行", url: "https://jegocloud.com/", desc: "即时通讯与云端协作工具，配套浏览器扩展", tags: "通讯,协作", free: "完全免费" },
        { name: "GreasyFork 脚本库", url: "https://greasyfork.org/zh-CN", desc: "油猴脚本最大中文仓库，配合 Tampermonkey 使用", tags: "油猴脚本,仓库", free: "完全免费" },
        { name: "ScriptCat 脚本猫", url: "https://scriptcat.org/", desc: "开源用户脚本管理器与脚本市场，国产替代方案", tags: "脚本市场,开源", free: "完全免费" },
        { name: "uBlock Origin", url: "https://github.com/gorhill/uBlock", desc: "最受欢迎的开源广告拦截扩展，性能优于同类", tags: "开源,广告拦截", free: "完全免费" }
      ]
    },
    {
      id: "wallpaper", name: "壁纸 · 图库站", icon: "🖼️",
      tools: [
        { name: "Wallhaven", url: "https://wallhaven.cc/", desc: "资源超 120 万张，可按分辨率/标签/色系精确筛选", tags: "量最大,精确筛选", free: "完全免费" },
        { name: "哲风壁纸", url: "https://haowallpaper.com/", desc: "4K/8K 高清壁纸，分类全覆盖，支持分辨率筛选", tags: "4K/8K,国内快", free: "完全免费" },
        { name: "极简壁纸", url: "https://bz.zzzmh.cn/", desc: "国内访问快，壁纸源自 Wallhaven 并重新归类", tags: "国内快,免登录", free: "完全免费" },
        { name: "壁纸汇", url: "https://www.bizhihui.com/", desc: "11000+ 4K/8K 壁纸，分类清晰无需登录", tags: "4K/8K,量足", free: "完全免费" },
        { name: "WallpaperHub", url: "https://wallpaperhub.app/", desc: "精选 Surface/Bing 官方壁纸，多设备尺寸适配", tags: "官方精选,多尺寸", free: "完全免费" },
        { name: "Wallpaper Abyss", url: "https://wall.alphacoders.com/", desc: "中文界面，影视/动漫壁纸丰富，支持搜索", tags: "影视动漫,中文", free: "完全免费" },
        { name: "AURA 壁纸", url: "https://gallery.wallaura.cn/", desc: "国内高清聚合站，覆盖风光/动漫/极简/AI 生成", tags: "风格全", free: "免费(含广告)" },
        { name: "WallpapersCraft", url: "https://wallpaperscraft.com/", desc: "97000+ 桌面壁纸，按分辨率与标签筛选", tags: "量足", free: "完全免费" },
        { name: "Bing 每日壁纸", url: "https://bing.ioliu.cn/", desc: "必应每日壁纸归档，可查任意日期并下载 4K", tags: "必应,可回溯", free: "完全免费" },
        { name: "故宫壁纸", url: "https://www.dpm.org.cn/lights/royal.html", desc: "故宫官方国风文物高清壁纸，古韵高级", tags: "官方,国风", free: "完全免费" },
        { name: "Moviemania", url: "https://moviemania.io/", desc: "国外电影无字幕壁纸，氛围感拉满", tags: "电影壁纸", free: "完全免费" },
        { name: "Konachan", url: "https://konachan.net/", desc: "专注二次元插画壁纸，无水印可右键保存", tags: "二次元", free: "完全免费" }
      ]
    },
    {
      id: "stock-photo", name: "免费图库 · 素材", icon: "📷",
      tools: [
        { name: "Pexels", url: "https://www.pexels.com/zh-cn/", desc: "免费商用高清图库，图片与视频素材兼具", tags: "免费商用,含视频", free: "完全免费" },
        { name: "Unsplash", url: "https://unsplash.com/", desc: "全球最大免费高清图库，摄影级素材资源", tags: "摄影级,免费商用", free: "完全免费" },
        { name: "Pixabay", url: "https://pixabay.com/zh/", desc: "图片/插画/矢量/视频/音乐全类型免费素材", tags: "全类型,免费商用", free: "完全免费" },
        { name: "Freepik", url: "https://www.freepik.com/", desc: "矢量图/PSD/图标素材库，设计资源丰富", tags: "矢量图,设计素材", free: "免费额度" },
        { name: "Stocksnap", url: "https://stocksnap.io/", desc: "CC0 协议高分辨率摄影图库，无需署名", tags: "CC0,免署名", free: "完全免费" },
        { name: "FoodiesFeed", url: "https://www.foodiesfeed.com/", desc: "专注美食摄影的免费图库，商用无需授权", tags: "美食,免费商用", free: "完全免费" },
        { name: "PxHere", url: "https://pxhere.com/", desc: "CC0 免费图片站，支持中文界面与筛选", tags: "CC0,中文", free: "完全免费" },
        { name: "致美化", url: "https://zhutix.com/", desc: "国内视觉美化社区，主题/壁纸/图标/皮肤素材丰富", tags: "主题美化,社区", free: "免费为主" },
        { name: "Lively Wallpaper", url: "https://www.rocksdanister.com/lively/", desc: "开源动态壁纸软件，GIF/视频/网页设为桌面壁纸", tags: "开源,动态壁纸", free: "完全免费" }
      ]
    },
    {
      id: "email", name: "邮箱 · 服务商", icon: "📧",
      tools: [
        { name: "Gmail", url: "https://mail.google.com/", desc: "谷歌邮箱，15GB 空间，全球通用（需网络条件）", tags: "国际主流", free: "完全免费" },
        { name: "Outlook", url: "https://outlook.live.com/mail/0/", desc: "微软邮箱，与 Office 生态深度集成", tags: "国际主流", free: "完全免费" },
        { name: "QQ 邮箱", url: "https://wx.mail.qq.com/", desc: "国内最普及的邮箱，支持多账号聚合与微信提醒", tags: "国内主流", free: "完全免费" },
        { name: "163 邮箱", url: "https://mail.163.com/", desc: "网易邮箱，国内老牌，反垃圾能力强", tags: "国内老牌", free: "完全免费" },
        { name: "126 邮箱", url: "https://mail.126.com/", desc: "网易旗下邮箱，与 163 同源，界面更简洁", tags: "国内老牌", free: "完全免费" },
        { name: "188 邮箱", url: "https://www.188.com/", desc: "网易旗下商务邮箱", tags: "商务", free: "完全免费" },
        { name: "阿里邮箱", url: "https://mail.aliyun.com/", desc: "阿里云个人邮箱，国内访问稳定，支持多域名", tags: "阿里系", free: "完全免费" },
        { name: "新浪邮箱", url: "https://mail.sina.com.cn/", desc: "新浪邮箱，国内老牌服务", tags: "国内老牌", free: "完全免费" },
        { name: "TOM 邮箱", url: "https://mail.tom.com/", desc: "国内老牌邮箱，含企业邮箱服务", tags: "国内老牌", free: "完全免费" },
        { name: "21CN 邮箱", url: "https://mail.21cn.com/", desc: "世纪龙旗下邮箱，广东地区用户较多", tags: "国内老牌", free: "完全免费" },
        { name: "139 邮箱", url: "https://mail.10086.cn/", desc: "中国移动旗下，支持短信提醒与手机号邮箱", tags: "移动系", free: "完全免费" },
        { name: "189 邮箱", url: "https://webmail30.189.cn/", desc: "中国电信天翼邮箱", tags: "电信系", free: "完全免费" },
        { name: "沃邮箱", url: "https://mail.wo.cn/", desc: "中国联通旗下邮箱服务", tags: "联通系", free: "完全免费" },
        { name: "企业微信邮箱", url: "https://work.exmail.qq.com/", desc: "腾讯企业邮箱，与企微/微信互通", tags: "企业协同", free: "免费版" },
        { name: "263 邮箱", url: "https://www.263.net/", desc: "国内企业邮箱服务商，兼顾个人邮箱", tags: "企业邮箱", free: "免费额度" }
      ]
    },
    {
      id: "email-temp", name: "临时邮箱工具", icon: "📨",
      tools: [
        { name: "Temp-Mail", url: "https://temp-mail.org/", desc: "知名度最高的临时邮箱，有 App 与浏览器扩展", tags: "临时邮箱,有App", free: "完全免费" },
        { name: "Mail.tm", url: "https://mail.tm/zh/", desc: "临时邮箱含公开 REST API，开发者友好", tags: "临时邮箱,有API", free: "完全免费" },
        { name: "10 分钟邮箱", url: "https://10minutemail.com/", desc: "经典 10 分钟自毁邮箱，地址不与他人共用可延长", tags: "临时邮箱,可延长", free: "完全免费" },
        { name: "Maildrop", url: "https://maildrop.cc/", desc: "可自定义地址，内置 Heluna 反垃圾过滤，零广告", tags: "临时邮箱,零广告", free: "完全免费" },
        { name: "Guerrilla Mail", url: "https://www.guerrillamail.com/zh/", desc: "老牌临时邮箱，少见的支持发信与附件的服务", tags: "临时邮箱,可发信", free: "完全免费" },
        { name: "Moakt", url: "https://moakt.com/zh", desc: "随机邮箱服务，可自定义地址，界面清爽", tags: "临时邮箱", free: "完全免费" },
        { name: "Tempmail Plus", url: "https://tempmail.plus/zh/", desc: "临时邮箱+自定义域名，支持多域名切换", tags: "临时邮箱,多域名", free: "完全免费" },
        { name: "22.do", url: "https://22.do/", desc: "临时谷歌邮箱，可接收 Gmail 风格地址邮件", tags: "临时邮箱", free: "完全免费" },
        { name: "Mail.td", url: "https://mail.td/zh", desc: "临时邮箱服务，中文界面，支持多域名", tags: "临时邮箱", free: "完全免费" }
      ]
    }
  ]
}
];
