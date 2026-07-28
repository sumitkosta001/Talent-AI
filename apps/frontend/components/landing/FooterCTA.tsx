import React from 'react';
import Link from 'next/link';

export default function FooterCTA() {
  return (
    <section className="py-24 bg-[#2563EB]">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 text-center">
        <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
          Ready to transform your hiring?
        </h2>
        <p className="text-blue-200 mb-8">
          Join over 50,000 companies and candidates already using TalentAI.
        </p>
        <div className="flex flex-col sm:flex-row gap-3 justify-center">
          <Link
            href="/register"
            className="bg-white text-[#2563EB] px-6 py-3 rounded-xl font-semibold hover:bg-blue-50 transition-colors"
          >
            Start for Free
          </Link>
          <Link
            href="/login"
            className="border border-blue-400 text-white px-6 py-3 rounded-xl font-semibold hover:bg-blue-700 transition-colors"
          >
            Login
          </Link>
        </div>
      </div>
    </section>
  );
}
