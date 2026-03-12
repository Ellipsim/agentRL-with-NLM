

(define (problem BW-rand-12)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 )
(:init
(arm-empty)
(on b1 b5)
(on b2 b6)
(on b3 b8)
(on b4 b1)
(on b5 b12)
(on-table b6)
(on-table b7)
(on b8 b4)
(on-table b9)
(on b10 b7)
(on b11 b3)
(on b12 b9)
(clear b2)
(clear b10)
(clear b11)
)
(:goal
(and
(on b1 b11)
(on b2 b7)
(on b3 b10)
(on b4 b2)
(on b5 b9)
(on b7 b1)
(on b10 b4)
(on b11 b6)
(on b12 b8))
)
)


