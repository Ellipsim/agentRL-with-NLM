

(define (problem BW-rand-10)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 )
(:init
(arm-empty)
(on b1 b6)
(on-table b2)
(on b3 b9)
(on b4 b2)
(on b5 b3)
(on-table b6)
(on b7 b1)
(on b8 b10)
(on b9 b8)
(on-table b10)
(clear b4)
(clear b5)
(clear b7)
)
(:goal
(and
(on b1 b5)
(on b3 b10)
(on b4 b7)
(on b5 b6)
(on b6 b3)
(on b7 b1)
(on b9 b2)
(on b10 b8))
)
)


