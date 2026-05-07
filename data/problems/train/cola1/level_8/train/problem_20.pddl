

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b3)
(on b2 b1)
(ontable b3)
(on b4 b9)
(on b5 b7)
(on b6 b5)
(ontable b7)
(ontable b8)
(ontable b9)
(on b10 b4)
(clear b2)
(clear b6)
(clear b8)
(clear b10)
)
(:goal
(and
(on b2 b4)
(on b3 b1)
(on b4 b9)
(on b5 b7)
(on b6 b2)
(on b7 b10)
(on b8 b5)
(on b9 b3)
(on b10 b6))
)
)


