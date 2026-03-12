

(define (problem BW-rand-12)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 )
(:init
(arm-empty)
(on b1 b2)
(on b2 b12)
(on-table b3)
(on b4 b10)
(on b5 b3)
(on-table b6)
(on b7 b9)
(on b8 b6)
(on-table b9)
(on b10 b8)
(on b11 b1)
(on b12 b5)
(clear b4)
(clear b7)
(clear b11)
)
(:goal
(and
(on b1 b4)
(on b2 b10)
(on b3 b8)
(on b4 b6)
(on b7 b3)
(on b8 b12)
(on b10 b5)
(on b11 b2)
(on b12 b11))
)
)


