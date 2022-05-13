package com.capstone.nft.ui.activity.main

import android.os.Bundle
import androidx.activity.viewModels
import androidx.core.view.get
import androidx.databinding.DataBindingUtil
import com.capstone.nft.R
import com.capstone.nft.base.BaseActivity
import com.capstone.nft.databinding.ActivityMainBinding
import com.capstone.nft.ui.adapter.main.MainAdapter
import com.capstone.nft.viewmodel.MainViewModel
import com.google.android.material.tabs.TabLayout
import com.google.android.material.tabs.TabLayoutMediator

class MainActivity : BaseActivity() {
    lateinit var mBinding: ActivityMainBinding
    lateinit var mAdapter: MainAdapter
    val mViewModel: MainViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        mBinding = DataBindingUtil.setContentView(this, R.layout.activity_main)

        setLayout()
        setObserve()
    }

    fun setLayout() {
        mAdapter = MainAdapter(this)
        mBinding.amVpPager.adapter = mAdapter

        TabLayoutMediator(
            mBinding.amTlTab,
            mBinding.amVpPager
        ) { tab: TabLayout.Tab, pos: Int ->
            when (pos) {
                0 -> {
                    tab.text = "My"
                }
                1 -> {
                    tab.text = "Gallery"
                }
                2 -> {
                    tab.text = "More"
                }
            }
        }.attach()
    }

    fun setObserve(){
        mViewModel.mldGallery.observe(this){
            mBinding.amVpPager.get(0)
        }
    }
}