

(define (problem BW-rand-12)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 )
(:init
(arm-empty)
(on b1 b10)
(on b2 b9)
(on-table b3)
(on b4 b5)
(on b5 b8)
(on b6 b7)
(on b7 b2)
(on b8 b6)
(on b9 b12)
(on-table b10)
(on b11 b3)
(on-table b12)
(clear b1)
(clear b4)
(clear b11)
)
(:goal
(and
(on b1 b9)
(on b4 b6)
(on b6 b7)
(on b7 b8)
(on b8 b3)
(on b9 b4)
(on b11 b10)
(on b12 b11))
)
)


