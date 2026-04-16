(set-logic ALL)
; Constraint ID: c5d24cbe49c63ead
; Generated at: 2026-04-16 11:03:34
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59719)) (False)
(assert (not (= x 59719)))

; Query: ((== x 59720)) (False)
(assert (not (not (= x 59720))))

(check-sat)
(get-model)
