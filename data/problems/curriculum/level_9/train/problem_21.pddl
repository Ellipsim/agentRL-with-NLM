

(define (problem BW-rand-10)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 )
(:init
(arm-empty)
(on b1 b9)
(on b2 b4)
(on b3 b2)
(on-table b4)
(on-table b5)
(on-table b6)
(on-table b7)
(on b8 b10)
(on b9 b8)
(on b10 b7)
(clear b1)
(clear b3)
(clear b5)
(clear b6)
)
(:goal
(and
(on b1 b4)
(on b3 b7)
(on b4 b3)
(on b5 b2)
(on b6 b5)
(on b7 b9)
(on b8 b6)
(on b9 b10))
)
)


