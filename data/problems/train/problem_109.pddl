

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b2)
(on b2 b5)
(ontable b3)
(on b4 b1)
(on b5 b10)
(ontable b6)
(on b7 b8)
(on b8 b9)
(on b9 b3)
(ontable b10)
(clear b4)
(clear b6)
(clear b7)
)
(:goal
(and
(on b1 b7)
(on b2 b4)
(on b3 b8)
(on b4 b6)
(on b5 b3)
(on b7 b5)
(on b8 b9)
(on b9 b10))
)
)


