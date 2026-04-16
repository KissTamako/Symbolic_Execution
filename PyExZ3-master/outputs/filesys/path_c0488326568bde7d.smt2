(set-logic ALL)
; Path ID: c0488326568bde7d
; Generated at: 2026-04-16 11:29:08
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59986)) (False)
(assert (not (not (= x 59986))))

(check-sat)
(get-model)
