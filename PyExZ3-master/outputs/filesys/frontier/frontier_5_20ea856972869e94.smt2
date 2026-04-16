(set-logic ALL)
; Frontier Constraint ID: 20ea856972869e94
; Generated at: 2026-04-16 14:44:34
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 718)) (False)
(assert (not (= x 718)))

; Query: ((== x 719)) (False)
(assert (not (not (= x 719))))

(check-sat)
(get-model)
