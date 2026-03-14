

(define (problem BW-rand-12)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 )
(:init
(arm-empty)
(on b1 b4)
(on-table b2)
(on-table b3)
(on b4 b6)
(on-table b5)
(on b6 b7)
(on b7 b12)
(on b8 b5)
(on-table b9)
(on-table b10)
(on b11 b2)
(on-table b12)
(clear b1)
(clear b3)
(clear b8)
(clear b9)
(clear b10)
(clear b11)
)
(:goal
(and
(on b1 b8)
(on b3 b5)
(on b7 b6)
(on b8 b10)
(on b9 b3)
(on b12 b7))
)
)


