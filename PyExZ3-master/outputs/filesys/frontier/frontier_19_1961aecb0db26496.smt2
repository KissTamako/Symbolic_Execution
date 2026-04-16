(set-logic ALL)
; Constraint ID: 1961aecb0db26496
; Generated at: 2026-04-16 04:08:23
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59263)) (False)
(assert (not (= x 59263)))

; Query: ((== x 59264)) (False)
(assert (not (not (= x 59264))))

(check-sat)
(get-model)
