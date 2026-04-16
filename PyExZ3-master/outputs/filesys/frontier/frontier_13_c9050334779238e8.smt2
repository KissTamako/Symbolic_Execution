(set-logic ALL)
; Constraint ID: c9050334779238e8
; Generated at: 2026-04-16 11:29:08
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60004)) (False)
(assert (not (= x 60004)))

; Query: ((== x 60005)) (False)
(assert (not (not (= x 60005))))

(check-sat)
(get-model)
