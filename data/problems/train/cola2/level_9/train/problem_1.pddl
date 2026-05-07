

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(ontable b1)
(on b2 b8)
(ontable b3)
(on b4 b1)
(on b5 b11)
(on b6 b10)
(ontable b7)
(ontable b8)
(ontable b9)
(ontable b10)
(on b11 b9)
(clear b2)
(clear b3)
(clear b4)
(clear b5)
(clear b6)
(clear b7)
)
(:goal
(and
(on b1 b5)
(on b2 b11)
(on b4 b2)
(on b6 b7)
(on b7 b3)
(on b9 b8)
(on b10 b9)
(on b11 b6))
)
)


