

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b6)
(ontable b2)
(on b3 b7)
(on b4 b10)
(ontable b5)
(on b6 b3)
(on b7 b4)
(ontable b8)
(on b9 b2)
(on b10 b9)
(clear b1)
(clear b5)
(clear b8)
)
(:goal
(and
(on b1 b10)
(on b2 b7)
(on b3 b4)
(on b4 b2)
(on b6 b5)
(on b7 b1)
(on b9 b6)
(on b10 b8))
)
)


