

(define (problem BW-rand-13)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 b13 )
(:init
(arm-empty)
(on b1 b9)
(on b2 b4)
(on b3 b12)
(on-table b4)
(on b5 b11)
(on b6 b7)
(on b7 b1)
(on-table b8)
(on b9 b3)
(on b10 b13)
(on b11 b10)
(on-table b12)
(on b13 b8)
(clear b2)
(clear b5)
(clear b6)
)
(:goal
(and
(on b1 b13)
(on b2 b9)
(on b4 b3)
(on b5 b1)
(on b6 b10)
(on b7 b6)
(on b8 b12)
(on b12 b7)
(on b13 b11))
)
)


