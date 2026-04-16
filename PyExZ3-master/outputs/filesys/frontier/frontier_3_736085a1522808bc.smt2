(set-logic ALL)
; Frontier Constraint ID: 736085a1522808bc
; Generated at: 2026-04-16 14:41:51
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 490)) (False)
(assert (not (= x 490)))

; Query: ((== x 491)) (False)
(assert (not (not (= x 491))))

(check-sat)
(get-model)
